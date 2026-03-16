"""
Utility functions for the Nordic Ski Webcams Telegram Bot.
"""

import re
import time
import logging
import urllib.request

from config import (
    PYRENEIGE_CAPCIR_URL,
    CAPCIR_WEBCAM_PREFIXES,
    WEBCAM_FETCH_TIMEOUT,
    USER_AGENT,
)

logger = logging.getLogger(__name__)


def get_capcir_webcam_url(station_id: str) -> str | None:
    """
    Fetch current Capcir webcam URL by scraping the timestamp from pyreneige.fr.

    The Capcir webcams use dynamic timestamps that change with each update.
    This function scrapes the current timestamp and constructs the full URL.

    Args:
        station_id: The station identifier ('llose' or 'quillane')

    Returns:
        The full webcam URL with current timestamp, or None if scraping fails
    """
    prefix = CAPCIR_WEBCAM_PREFIXES.get(station_id)
    if not prefix:
        return None

    try:
        req = urllib.request.Request(
            PYRENEIGE_CAPCIR_URL,
            headers={'User-Agent': USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=WEBCAM_FETCH_TIMEOUT) as response:
            html = response.read().decode('utf-8')

        # Pattern: capcir-coldelallose_2026-02-05-14-35-289.jpg
        pattern = rf'{prefix}_(\d{{4}}-\d{{2}}-\d{{2}}-\d{{2}}-\d{{2}}-\d+)\.jpg'
        match = re.search(pattern, html)

        if match:
            timestamp = match.group(1)
            return f"https://www.pyreneige.fr/webcams/{prefix}_{timestamp}.jpg"

    except urllib.error.URLError as e:
        logger.error(f"Network error fetching Capcir webcam URL for {station_id}: {e}")
    except TimeoutError:
        logger.error(f"Timeout fetching Capcir webcam URL for {station_id}")
    except Exception as e:
        logger.error(f"Error fetching Capcir webcam URL for {station_id}: {e}")

    return None


def add_cache_buster(url: str) -> str:
    """
    Add a cache-busting timestamp parameter to a URL.

    This forces Telegram to fetch a fresh image instead of using cached version.

    Args:
        url: The original URL

    Returns:
        URL with cache-busting parameter added
    """
    cache_buster = int(time.time())
    if '?' in url:
        return f"{url}&_t={cache_buster}"
    return f"{url}?_t={cache_buster}"


def get_webcam_url(station_id: str, station_data: dict) -> str | None:
    """
    Get the webcam URL for a station, handling special cases.

    Args:
        station_id: The station identifier
        station_data: The station data dictionary

    Returns:
        The webcam URL (with cache-busting if applicable), or None if unavailable
    """
    if station_data.get("requires_scraping"):
        return get_capcir_webcam_url(station_id)

    webcam_url = station_data.get("webcam")
    if webcam_url:
        return add_cache_buster(webcam_url)

    return None
