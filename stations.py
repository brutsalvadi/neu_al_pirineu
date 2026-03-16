"""
Station data for Nordic ski stations in the Pyrenees.

Each station has:
- name: Display name
- region: Geographic region
- km_open: Currently open km / total km (static fallback, may be overridden by live data)
- snow: Snow depth (static fallback, may be overridden by live data)
- webcam: Direct webcam image URL
- url: Official webcam page URL
- aliases: Command aliases for the bot
- requires_scraping: If True, webcam URL needs dynamic scraping
- data_source: Where live conditions come from (see data_sources.py)

Data Sources:
- projecte4estacions: Catalan station webcams
- bergfex: French station webcams
- infonieve: General conditions (km, snow) - often outdated
- capcir_nordique: Capcir bulletin neige (km, snow) - daily updates
- pyreneige: Capcir webcam URLs (dynamic timestamps)
"""

STATIONS = {
    # ==========================================================================
    # PIRINEO CATALÁN (Spanish Catalan Pyrenees)
    # Webcams from: projecte4estacions.com
    # ==========================================================================
    "aransa": {
        "name": "Aransa",
        "region": "Pirineo Catalán",
        "km_open": "30/32",
        "snow": "150 cm",
        "webcam": "https://app.projecte4estacions.com/snapshots/aransa-estacio-data.jpg",
        "url": "https://www.totnordic.com/webcams/webcam-aransa/",
        "aliases": ["ara"]
    },
    "guils": {
        "name": "Guils Fontanera",
        "region": "Pirineo Catalán",
        "km_open": "-/33",
        "snow": "50 cm",
        "webcam": "https://app.projecte4estacions.com/snapshots/guils-data.jpg",
        "url": "https://www.guils.com/webcam/",
        "aliases": ["gui", "fontanera"]
    },
    "lles": {
        "name": "Lles de Cerdanya",
        "region": "Pirineo Catalán",
        "km_open": "28/34.2",
        "snow": "150 cm",
        "webcam": "https://app.projecte4estacions.com/snapshots/lles-estacio-data.jpg",
        "url": "https://lles.net/webcams/",
        "aliases": ["lle", "cerdanya"]
    },
    "santjoan": {
        "name": "Sant Joan de l'Erm",
        "region": "Pirineo Catalán",
        "km_open": "10/42",
        "snow": "100 cm",
        "webcam": "https://app.projecte4estacions.com/snapshots/santjoan-estacio-data.jpg",
        "url": "https://www.totnordic.com/webcams/webcam-sant-joan-de-lerm/",
        "aliases": ["sj", "erm", "santjoanlerm"]
    },
    "tavascan": {
        "name": "Tavascán (Nórdico)",
        "region": "Pirineo Catalán",
        "km_open": "-/15",
        "snow": "180 cm",
        "webcam": "https://app.projecte4estacions.com/imatge/tavascan-data.jpg",
        "url": "https://www.totnordic.com/webcams/webcam-tavascan/",
        "aliases": ["tav", "tava"]
    },
    "tuixent": {
        "name": "Tuixent - La Vansa",
        "region": "Pirineo Catalán",
        "km_open": "30/30",
        "snow": "210 cm",
        "webcam": "https://app.projecte4estacions.com/snapshots/tuixentlavansa-data.jpg",
        "url": "https://www.tuixent-lavansa.com/en-directe/",
        "aliases": ["tui", "vansa", "lavansa"]
    },
    "viros": {
        "name": "Virós-Vallferrera",
        "region": "Pirineo Catalán",
        "km_open": "-/20",
        "snow": "- cm",
        "webcam": "https://app.projecte4estacions.com/snapshots/viros-estacio-data.jpg",
        "url": "https://www.totnordic.com/webcams/webcam-viros-vallferrera/",
        "aliases": ["vir", "vallferrera"]
    },

    # ==========================================================================
    # ARIÈGE PYRÉNÉES (Southern France)
    # Webcams from: bergfex.at
    # ==========================================================================
    "beille": {
        "name": "Beille",
        "region": "Ariège Pyrénées",
        "km_open": "17.1/40.2",
        "snow": "120 cm",
        "webcam": "https://images.bergfex.at/webcams/?id=25058&format=4",
        "url": "https://www.beille.fr/webcams.html",
        "aliases": ["bei"]
    },
    "chioula": {
        "name": "Chioula",
        "region": "Ariège Pyrénées",
        "km_open": "23.7/48",
        "snow": "85 cm",
        "webcam": "https://images.bergfex.at/webcams/?id=23844&format=4",
        "url": "https://www.chioula.fr/webcams-chioula.html",
        "aliases": ["chi", "chio"]
    },

    # ==========================================================================
    # NEIGES CATALANES (French Catalan Pyrenees)
    # Capcir: Dynamic timestamps scraped from pyreneige.fr
    # Font-Romeu: bergfex.at
    # ==========================================================================
    "llose": {
        "name": "Capcir - Col de la Llose",
        "region": "Neiges Catalanes",
        "km_open": "65.5/65.5",  # Fallback; live data from capcir_nordique
        "snow": "125 cm",
        "webcam": "http://91.121.33.165/~cam/coldelallose.jpg",  # Fallback, actually scraped
        "url": "https://www.capcir-nordique.com/fr/accueil/webcams",
        "aliases": ["llos"],
        "requires_scraping": True,
        "data_source": "capcir_nordique",
    },
    "quillane": {
        "name": "Capcir - Col de la Quillane",
        "region": "Neiges Catalanes",
        "km_open": "21/21",  # Fallback; live data from capcir_nordique
        "snow": "125 cm",
        "webcam": "http://91.121.33.165/~cam/laquillane.jpg",  # Fallback, actually scraped
        "url": "https://www.capcir-nordique.com/fr/accueil/webcams",
        "aliases": ["quil", "qui"],
        "requires_scraping": True,
        "data_source": "capcir_nordique",
    },
    "matte": {
        "name": "Capcir - Forêt de la Matte",
        "region": "Neiges Catalanes",
        "km_open": "26.4/26.4",  # Fallback; live data from capcir_nordique
        "snow": "125 cm",
        "webcam": "http://91.121.33.165/~cam/coldelallose.jpg",  # Uses Llose webcam
        "url": "https://www.capcir-nordique.com/fr/accueil/webcams",
        "aliases": ["mat", "foret"],
        "requires_scraping": True,
        "data_source": "capcir_nordique",
    },
    "fontromeu": {
        "name": "Font-Romeu Pyrénées 2000",
        "region": "Neiges Catalanes",
        "km_open": "-/107.1",
        "snow": "100 cm",
        "webcam": "https://images.bergfex.at/webcams/?id=24391&format=4",  # Les Airelles
        "url": "https://www.bergfex.com/font-romeu/webcams/",
        "aliases": ["fr", "font", "romeu", "pyrenees2000", "p2000"]
    },
}


def build_alias_map() -> dict[str, str]:
    """Build reverse lookup map from aliases to station IDs."""
    alias_map = {}
    for station_id, data in STATIONS.items():
        alias_map[station_id] = station_id
        for alias in data.get("aliases", []):
            alias_map[alias] = station_id
    return alias_map


# Pre-built alias map for fast lookups
ALIAS_MAP = build_alias_map()


def get_station(query: str) -> dict | None:
    """Look up station by name or alias."""
    query = query.lower().strip()
    station_id = ALIAS_MAP.get(query)
    if station_id:
        return STATIONS[station_id]
    return None


def get_station_id(query: str) -> str | None:
    """Look up station ID by name or alias."""
    query = query.lower().strip()
    return ALIAS_MAP.get(query)


def get_stations_by_region() -> dict[str, list[tuple[str, dict]]]:
    """Get stations grouped by region."""
    regions: dict[str, list[tuple[str, dict]]] = {}
    for station_id, data in STATIONS.items():
        region = data["region"]
        if region not in regions:
            regions[region] = []
        regions[region].append((station_id, data))
    return regions


def requires_scraping(station_id: str) -> bool:
    """Check if a station requires webcam URL scraping."""
    station = STATIONS.get(station_id)
    return station.get("requires_scraping", False) if station else False
