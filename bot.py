#!/usr/bin/env python3
"""
Nordic Ski Webcams Telegram Bot

Provides current conditions and webcam images for Nordic ski stations
across the Catalan and French Pyrenees.

Supports:
- Polling mode (local development)
- Webhook mode (production on Fly.io)
- Multi-language: Spanish (default), Catalan, English

Usage:
    # Local development (polling)
    export TELEGRAM_BOT_TOKEN="your_token"
    python bot.py

    # Production (webhook)
    export TELEGRAM_BOT_TOKEN="your_token"
    export WEBHOOK_URL="https://your-app.fly.dev"
    python bot.py
"""

import logging
from datetime import time

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from config import TELEGRAM_BOT_TOKEN, WEBHOOK_URL, PORT
from stations import ALIAS_MAP
from handlers import (
    start,
    help_command,
    support_command,
    graciosillo_command,
    list_stations,
    all_stations,
    station_handler,
    lang_command,
    lang_callback,
    stats_command,
    admin_send_summary,
    send_weekly_summary,
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def create_application() -> Application:
    """Create and configure the bot application with all handlers."""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # General commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("support", support_command))
    application.add_handler(CommandHandler("donate", support_command))
    application.add_handler(CommandHandler("coffee", support_command))

    # Station listing commands
    application.add_handler(CommandHandler("list", list_stations))
    application.add_handler(CommandHandler("all", all_stations))
    application.add_handler(CommandHandler("summary", all_stations))
    application.add_handler(CommandHandler("resumen", all_stations))
    application.add_handler(CommandHandler("resum", all_stations))

    # Language commands
    application.add_handler(CommandHandler("lang", lang_command))
    application.add_handler(CallbackQueryHandler(lang_callback, pattern="^lang_"))

    # Graciosillo (funny) mode
    application.add_handler(CommandHandler("graciosillo", graciosillo_command))
    application.add_handler(CommandHandler("funny", graciosillo_command))
    application.add_handler(CommandHandler("payaso", graciosillo_command))

    # Admin/Stats commands
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("send_summary", admin_send_summary))

    # Station commands (dynamic based on station IDs and aliases)
    for cmd in set(ALIAS_MAP.keys()):
        application.add_handler(CommandHandler(cmd, station_handler))

    # Scheduled jobs
    # Every Friday at 13:00 UTC send summary to all users
    application.job_queue.run_daily(
        send_weekly_summary,
        time=time(13, 0),
        days=(4,),  # 0=Mon, 4=Fri
        name="weekly_summary",
    )

    return application


def main() -> None:
    """Start the bot in the appropriate mode based on environment."""
    application = create_application()

    if WEBHOOK_URL:
        # Webhook mode for production (Fly.io)
        logger.info(f"Starting bot in webhook mode on port {PORT}")
        logger.info(f"Webhook URL: {WEBHOOK_URL}")

        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="webhook",
            webhook_url=f"{WEBHOOK_URL}/webhook",
        )
    else:
        # Polling mode for local development
        logger.info("Starting bot in polling mode (local development)")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
