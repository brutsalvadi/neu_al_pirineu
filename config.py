"""
Configuration settings for the Nordic Ski Webcams Telegram Bot.
"""

import os

# Bot settings
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

# Admin user IDs (comma-separated in env, e.g. "12345,67890")
_admin_ids_str = os.environ.get("ADMIN_USER_IDS", "")
ADMIN_USER_IDS: set[int] = {int(x) for x in _admin_ids_str.split(",") if x.strip().isdigit()}

# Default language
DEFAULT_LANG = "es"

# Supported languages
SUPPORTED_LANGUAGES = ["es", "ca", "en"]

# Graciosillo mode (funny descriptions) - default off
DEFAULT_GRACIOSILLO = False

# Webcam scraping settings
WEBCAM_FETCH_TIMEOUT = 10  # seconds
USER_AGENT = "Mozilla/5.0"

# URLs
PYRENEIGE_CAPCIR_URL = "https://www.pyreneige.fr/espace-nordique/capcir/webcams/"
BUYMEACOFFEE_URL = "https://buymeacoffee.com/yourusername"

# Capcir webcam file prefixes (for scraping timestamps)
CAPCIR_WEBCAM_PREFIXES = {
    "llose": "capcir-coldelallose",
    "quillane": "capcir-coldelaquillane",
}
