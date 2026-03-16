"""
Data sources configuration and scraping logic for Nordic ski stations.

This module defines where data comes from for each station and provides
functions to fetch live data from various sources.

Data Sources:
- projecte4estacions: Catalan stations (webcams + some conditions)
- infonieve: General station data (km, snow) - fallback
- capcir-nordique: Capcir bulletin neige (km, snow for Llose/Quillane/Matte)
- bergfex: French station webcams
- pyreneige: Capcir webcam URLs (dynamic timestamps)
"""

import json
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger(__name__)


# =============================================================================
# DATA SOURCE DEFINITIONS
# =============================================================================

@dataclass
class DataSource:
    """Definition of a data source."""
    name: str
    url: str
    provides: list[str]  # What data it provides: "webcam", "km", "snow", etc.
    scrape_interval: int = 86400  # How often to scrape (seconds), default 24h


# All available data sources
DATA_SOURCES = {
    "projecte4estacions": DataSource(
        name="Projecte 4 Estacions",
        url="https://app.projecte4estacions.com",
        provides=["webcam"],
        scrape_interval=0,  # Direct image URLs, no scraping needed
    ),
    "bergfex": DataSource(
        name="Bergfex",
        url="https://images.bergfex.at",
        provides=["webcam"],
        scrape_interval=0,  # Direct image URLs
    ),
    "infonieve": DataSource(
        name="Infonieve",
        url="https://www.infonieve.es",
        provides=["km", "snow"],
        scrape_interval=86400,  # Once per day
    ),
    "capcir_nordique": DataSource(
        name="Capcir Nordique (Bulletin Neige)",
        url="https://www.capcir-nordique.com/bulletin-neige",
        provides=["km", "snow"],
        scrape_interval=86400,  # Once per day
    ),
    "pyreneige": DataSource(
        name="Pyreneige",
        url="https://www.pyreneige.fr/espace-nordique/capcir/webcams/",
        provides=["webcam"],
        scrape_interval=300,  # Every 5 minutes (dynamic timestamps)
    ),
}


# Station to data source mapping
# Defines where each piece of data comes from for each station
STATION_SOURCES = {
    # Pirineo Catalán - webcams from projecte4estacions, conditions from infonieve
    "aransa": {
        "webcam": "projecte4estacions",
        "km": "infonieve",
        "snow": "infonieve",
    },
    "guils": {
        "webcam": "projecte4estacions",
        "km": "infonieve",
        "snow": "infonieve",
    },
    "lles": {
        "webcam": "projecte4estacions",
        "km": "infonieve",
        "snow": "infonieve",
    },
    "santjoan": {
        "webcam": "projecte4estacions",
        "km": "infonieve",
        "snow": "infonieve",
    },
    "tavascan": {
        "webcam": "projecte4estacions",
        "km": "infonieve",
        "snow": "infonieve",
    },
    "tuixent": {
        "webcam": "projecte4estacions",
        "km": "infonieve",
        "snow": "infonieve",
    },
    "viros": {
        "webcam": "projecte4estacions",
        "km": "infonieve",
        "snow": "infonieve",
    },
    # Ariège - webcams from bergfex, conditions from infonieve
    "beille": {
        "webcam": "bergfex",
        "km": "infonieve",
        "snow": "infonieve",
    },
    "chioula": {
        "webcam": "bergfex",
        "km": "infonieve",
        "snow": "infonieve",
    },
    # Neiges Catalanes - Capcir from capcir-nordique + pyreneige
    "llose": {
        "webcam": "pyreneige",
        "km": "capcir_nordique",
        "snow": "capcir_nordique",
    },
    "quillane": {
        "webcam": "pyreneige",
        "km": "capcir_nordique",
        "snow": "capcir_nordique",
    },
    "matte": {
        "webcam": "pyreneige",  # Uses Llose webcam as fallback
        "km": "capcir_nordique",
        "snow": "capcir_nordique",
    },
    # Font-Romeu - bergfex webcam, infonieve conditions
    "fontromeu": {
        "webcam": "bergfex",
        "km": "infonieve",
        "snow": "infonieve",
    },
}


# =============================================================================
# CACHED DATA STORAGE
# =============================================================================

# Cache file path
CACHE_DIR = Path(__file__).parent / "data"
CACHE_FILE = CACHE_DIR / "conditions_cache.json"


@dataclass
class CachedConditions:
    """Cached snow conditions data."""
    snow_depth: str = ""
    km_open: str = ""
    km_total: str = ""
    last_updated: str = ""
    source: str = ""


# In-memory cache
_conditions_cache: dict[str, CachedConditions] = {}
_last_scrape_time: dict[str, float] = {}


def _load_cache() -> None:
    """Load cached conditions from disk."""
    global _conditions_cache, _last_scrape_time

    if not CACHE_FILE.exists():
        return

    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)

        for station_id, cached in data.get("conditions", {}).items():
            _conditions_cache[station_id] = CachedConditions(**cached)

        _last_scrape_time = data.get("last_scrape_time", {})
        logger.info(f"Loaded conditions cache for {len(_conditions_cache)} stations")
    except Exception as e:
        logger.error(f"Error loading cache: {e}")


def _save_cache() -> None:
    """Save cached conditions to disk."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        data = {
            "conditions": {
                station_id: {
                    "snow_depth": c.snow_depth,
                    "km_open": c.km_open,
                    "km_total": c.km_total,
                    "last_updated": c.last_updated,
                    "source": c.source,
                }
                for station_id, c in _conditions_cache.items()
            },
            "last_scrape_time": _last_scrape_time,
        }

        with open(CACHE_FILE, "w") as f:
            json.dump(data, f, indent=2)

        logger.info("Saved conditions cache")
    except Exception as e:
        logger.error(f"Error saving cache: {e}")


# Load cache on module import
_load_cache()


# =============================================================================
# CAPCIR BULLETIN NEIGE SCRAPING
# =============================================================================

# Domain km totals (from official bulletin neige)
CAPCIR_DOMAINS = {
    "llose": {
        "name": "Domaine de La Llose",
        "km_total": 65.5,
        "trails": [
            "La jassa de Catlla", "Le Dourmidou", "Le Cortal",
            "La Llosette", "Refuge du Torn", "Clavera", "Col de Creu/Refuge du Torn"
        ],
    },
    "quillane": {
        "name": "Domaine de la Quillane",
        "km_total": 21.0,
        "trails": ["Calvet", "Calvet la Serre"],
    },
    "matte": {
        "name": "Domaine de la Forêt de la Matte",
        "km_total": 26.4,
        "trails": ["Vora de la Mata", "La Barrancosa", "La Matte", "Le Canal"],
    },
}


def _scrape_capcir_bulletin() -> dict[str, Any] | None:
    """
    Scrape snow conditions from capcir-nordique.com bulletin neige.

    Returns dict with:
    - snow_depth: str (e.g., "125 cm")
    - status: str (e.g., "STATION NORDIQUE OUVERTE")
    - domains: dict with per-domain open/closed status
    """
    url = "https://www.capcir-nordique.com/bulletin-neige"

    try:
        with httpx.Client(timeout=15.0, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            html = response.text

        result = {
            "snow_depth": "",
            "status": "",
            "all_open": False,
            "scraped_at": datetime.now().isoformat(),
        }

        # Extract snow depth (look for patterns like "125cm" or "125 cm")
        snow_match = re.search(r'(\d+)\s*cm', html, re.IGNORECASE)
        if snow_match:
            result["snow_depth"] = f"{snow_match.group(1)} cm"

        # Check if station is open
        if "OUVERTE" in html.upper():
            result["status"] = "OUVERTE"
            result["all_open"] = True
        elif "FERMÉE" in html.upper() or "FERMEE" in html.upper():
            result["status"] = "FERMÉE"
            result["all_open"] = False

        # Check for "toutes les pistes" (all trails) status
        if "toutes les pistes sont damées" in html.lower():
            result["all_open"] = True

        logger.info(f"Scraped Capcir bulletin: {result['snow_depth']}, status={result['status']}")
        return result

    except Exception as e:
        logger.error(f"Error scraping Capcir bulletin: {e}")
        return None


def update_capcir_conditions(force: bool = False) -> bool:
    """
    Update cached conditions for Capcir stations from bulletin neige.

    Args:
        force: If True, scrape even if cache is fresh

    Returns:
        True if update was successful
    """
    source_key = "capcir_nordique"
    now = time.time()

    # Check if we need to scrape
    last_scrape = _last_scrape_time.get(source_key, 0)
    interval = DATA_SOURCES[source_key].scrape_interval

    if not force and (now - last_scrape) < interval:
        logger.debug("Capcir cache still fresh, skipping scrape")
        return True

    # Scrape bulletin
    bulletin = _scrape_capcir_bulletin()
    if not bulletin:
        return False

    # Update conditions for each Capcir domain
    snow = bulletin.get("snow_depth", "- cm")
    all_open = bulletin.get("all_open", False)

    for domain_id, domain_info in CAPCIR_DOMAINS.items():
        km_total = domain_info["km_total"]

        # If all open, km_open = km_total, otherwise unknown
        if all_open:
            km_open = str(km_total)
        else:
            km_open = "-"

        _conditions_cache[domain_id] = CachedConditions(
            snow_depth=snow,
            km_open=km_open,
            km_total=str(km_total),
            last_updated=bulletin.get("scraped_at", ""),
            source=source_key,
        )

    _last_scrape_time[source_key] = now
    _save_cache()

    return True


# =============================================================================
# PUBLIC API
# =============================================================================

def get_station_conditions(station_id: str) -> CachedConditions | None:
    """
    Get cached conditions for a station.

    For Capcir stations, triggers daily scrape if needed.
    """
    sources = STATION_SOURCES.get(station_id)
    if not sources:
        return None

    # Check if this station uses capcir_nordique for conditions
    if sources.get("km") == "capcir_nordique":
        # Trigger update if needed (once per day)
        update_capcir_conditions()

    return _conditions_cache.get(station_id)


def get_conditions_display(station_id: str) -> tuple[str, str]:
    """
    Get display strings for km_open and snow for a station.

    Returns:
        Tuple of (km_open_str, snow_str) e.g., ("65.5/65.5", "125 cm")
    """
    conditions = get_station_conditions(station_id)

    if conditions and conditions.km_open:
        km_str = f"{conditions.km_open}/{conditions.km_total}"
        snow_str = conditions.snow_depth
        return km_str, snow_str

    # Return None to indicate fallback to static data
    return None, None


def get_data_source_info(station_id: str) -> dict[str, str]:
    """Get information about where data comes from for a station."""
    sources = STATION_SOURCES.get(station_id, {})
    return {
        data_type: DATA_SOURCES[source_name].name
        for data_type, source_name in sources.items()
        if source_name in DATA_SOURCES
    }


def get_source_for_station(station_id: str, data_type: str) -> str | None:
    """Get the source name for a specific data type of a station."""
    sources = STATION_SOURCES.get(station_id, {})
    return sources.get(data_type)


def force_refresh_all() -> dict[str, bool]:
    """Force refresh of all scraped data sources."""
    results = {}

    # Capcir
    results["capcir_nordique"] = update_capcir_conditions(force=True)

    # Add other sources here as needed

    return results
