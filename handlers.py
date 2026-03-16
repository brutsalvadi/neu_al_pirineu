"""
Telegram bot command handlers for the Nordic Ski Webcams Bot.
"""

import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_USER_IDS
from translations import t, set_user_lang, get_user_lang, TRANSLATIONS
from stations import STATIONS, ALIAS_MAP, get_stations_by_region
from utils import get_webcam_url
from graciosillo import (
    is_graciosillo_enabled,
    toggle_graciosillo,
    get_funny_snow_description,
    get_funny_km_description,
    get_random_comment,
)
from analytics import log_command, get_stats_summary, get_all_user_ids
from ratelimit import check_rate_limit, record_command, get_abuse_summary
from data_sources import get_conditions_display, get_data_source_info

logger = logging.getLogger(__name__)


def _log(update: Update, command: str) -> None:
    """Helper to log command with user info."""
    user = update.effective_user
    if user:
        log_command(user.id, user.username, command)


async def _check_rate_limit(update: Update) -> bool:
    """
    Check rate limit for user. If blocked, sends error message.

    Returns:
        True if allowed, False if blocked
    """
    user = update.effective_user
    if not user:
        return True

    allowed, message = check_rate_limit(user.id)
    if not allowed:
        await update.message.reply_text(message)
        return False

    record_command(user.id)
    return True


# =============================================================================
# GENERAL COMMANDS
# =============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with available commands."""
    if not await _check_rate_limit(update):
        return
    _log(update, "start")
    user_id = update.effective_user.id

    station_list = "\n".join([
        f"  /{sid} - {data['name']}"
        for sid, data in STATIONS.items()
    ])

    await update.message.reply_text(
        f"{t(user_id, 'welcome_title')}\n\n"
        f"{t(user_id, 'welcome_desc')}\n\n"
        f"{t(user_id, 'available_stations')}\n{station_list}\n\n"
        f"{t(user_id, 'example')} /tuixent o /tui\n\n"
        f"{t(user_id, 'use_help')}",
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message with all available commands."""
    if not await _check_rate_limit(update):
        return
    _log(update, "help")
    user_id = update.effective_user.id

    aliases_info = []
    for sid, data in STATIONS.items():
        aliases = ", ".join([f"/{a}" for a in data.get("aliases", [])])
        if aliases:
            aliases_info.append(f"/{sid} → {aliases}")

    # Show graciosillo status
    graciosillo_status = t(user_id, 'graciosillo_status_on') if is_graciosillo_enabled(user_id) else t(user_id, 'graciosillo_status_off')

    await update.message.reply_text(
        f"{t(user_id, 'help_title')}\n\n"
        f"{t(user_id, 'commands')}\n"
        f"{t(user_id, 'cmd_start')}\n"
        f"{t(user_id, 'cmd_help')}\n"
        f"{t(user_id, 'cmd_list')}\n"
        f"{t(user_id, 'cmd_all')}\n"
        f"{t(user_id, 'cmd_lang')}\n"
        f"{t(user_id, 'cmd_graciosillo')}\n"
        f"{t(user_id, 'cmd_support')}\n\n"
        f"{graciosillo_status}\n\n"
        f"{t(user_id, 'station_shortcuts')}\n" + "\n".join(aliases_info) + "\n\n"
        f"{t(user_id, 'regions')}\n"
        f"{t(user_id, 'region_catalan')}\n"
        f"{t(user_id, 'region_ariege')}\n"
        f"{t(user_id, 'region_neiges')}",
        parse_mode='Markdown'
    )


async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show support/donation information."""
    if not await _check_rate_limit(update):
        return
    _log(update, "support")
    user_id = update.effective_user.id

    await update.message.reply_text(
        f"{t(user_id, 'support_title')}\n\n{t(user_id, 'support_text')}",
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


async def graciosillo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Toggle graciosillo (funny) mode."""
    if not await _check_rate_limit(update):
        return
    _log(update, "graciosillo")
    user_id = update.effective_user.id

    new_state = toggle_graciosillo(user_id)

    if new_state:
        await update.message.reply_text(
            t(user_id, 'graciosillo_enabled'),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            t(user_id, 'graciosillo_disabled'),
            parse_mode='Markdown'
        )


# =============================================================================
# STATION COMMANDS
# =============================================================================

async def list_stations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all stations grouped by region."""
    if not await _check_rate_limit(update):
        return
    _log(update, "list")
    user_id = update.effective_user.id

    regions = get_stations_by_region()

    message = f"{t(user_id, 'all_stations_title')}\n\n"
    for region, stations in regions.items():
        message += f"*{region}:*\n"
        message += "\n".join([f"/{sid} - {data['name']}" for sid, data in stations])
        message += "\n\n"

    await update.message.reply_text(message, parse_mode='Markdown')


async def all_stations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Quick text overview of all stations with conditions (summary)."""
    if not await _check_rate_limit(update):
        return
    _log(update, "all")
    user_id = update.effective_user.id

    regions = get_stations_by_region()
    message = f"{t(user_id, 'overview_title')}\n\n"

    for region, stations in regions.items():
        message += f"🏔️ *{region}*\n"
        for sid, data in stations:
            # Get live conditions if available
            live_km, live_snow = get_conditions_display(sid)
            km_open = live_km if live_km else data['km_open']
            snow = live_snow if live_snow else data['snow']
            message += f"  •  *{data['name']}*\n"
            message += f"      📏 {km_open} | ❄️ {snow}\n"
        message += "\n"

    await update.message.reply_text(message, parse_mode='Markdown')


async def station_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle station commands - send conditions and webcam image."""
    if not await _check_rate_limit(update):
        return
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    graciosillo = is_graciosillo_enabled(user_id)

    # Get command without the leading /
    command = update.message.text[1:].split('@')[0].lower()  # Handle @botname suffix

    # Resolve alias to station_id
    station_id = ALIAS_MAP.get(command)
    station = STATIONS.get(station_id) if station_id else None

    if not station:
        await update.message.reply_text(
            t(user_id, 'station_not_found').format(command)
        )
        return

    # Log the station command (use station_id for consistency)
    _log(update, station_id)

    # Get live conditions if available, otherwise use static data
    live_km, live_snow = get_conditions_display(station_id)
    km_open = live_km if live_km else station['km_open']
    snow = live_snow if live_snow else station['snow']

    # Check if we have unknown data (for graciosillo comments)
    has_unknown = "-" in km_open.split("/")[0] or "-" in snow

    # Build caption with station info
    if graciosillo:
        # Funny mode with creative descriptions
        funny_km = get_funny_km_description(km_open, lang)
        funny_snow = get_funny_snow_description(snow, lang)
        random_comment = get_random_comment(lang, has_unknown_data=has_unknown)

        caption = (
            f"🎿 *{station['name']}*\n"
            f"📍 {station['region']}\n\n"
            f"📏 {t(user_id, 'km_open')}: *{km_open}*\n"
            f"   ↳ _{funny_km}_\n"
            f"❄️ {t(user_id, 'snow')}: *{snow}*\n"
            f"   ↳ _{funny_snow}_\n\n"
            f"{random_comment}\n\n"
            f"[{t(user_id, 'more_webcams')}]({station['url']})"
        )
    else:
        # Normal mode
        caption = (
            f"🎿 *{station['name']}*\n"
            f"📍 {station['region']}\n\n"
            f"📏 {t(user_id, 'km_open')}: *{km_open}*\n"
            f"❄️ {t(user_id, 'snow')}: *{snow}*\n\n"
            f"[{t(user_id, 'more_webcams')}]({station['url']})"
        )

    try:
        webcam_url = get_webcam_url(station_id, station)
        if not webcam_url:
            raise Exception("Could not get webcam URL")

        # Send photo with caption
        await update.message.reply_photo(
            photo=webcam_url,
            caption=caption,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error sending photo for {station['name']}: {e}")
        # Fallback to text-only if image fails
        await update.message.reply_text(
            f"{caption}\n\n{t(user_id, 'image_error')}",
            parse_mode='Markdown'
        )


# =============================================================================
# LANGUAGE COMMANDS
# =============================================================================

async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show language selection menu."""
    if not await _check_rate_limit(update):
        return
    _log(update, "lang")
    user_id = update.effective_user.id

    keyboard = [
        [
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
            InlineKeyboardButton("🟨🟥 Català", callback_data="lang_ca"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"{t(user_id, 'lang_title')}\n\n{t(user_id, 'lang_current')}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language selection callback from inline keyboard."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang_code = query.data.replace("lang_", "")

    if set_user_lang(user_id, lang_code):
        await query.edit_message_text(
            text=t(user_id, 'lang_changed'),
            parse_mode='Markdown'
        )


# =============================================================================
# ADMIN COMMANDS
# =============================================================================

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show bot statistics (admin only - but we keep it simple, anyone can see)."""
    if not await _check_rate_limit(update):
        return
    _log(update, "stats")

    stats = get_stats_summary()
    abuse = get_abuse_summary()

    # Format top commands
    top_cmds = "\n".join([f"  /{cmd}: {count}" for cmd, count in stats['top_commands'][:5]])

    # Format peak hours
    peak_hrs = ", ".join([f"{h}:00" for h, _ in stats['peak_hours']])

    message = (
        "📊 *Bot Statistics*\n\n"
        f"👥 *Users*\n"
        f"  Total: {stats['total_users']}\n"
        f"  Active (7d): {stats['active_users_7d']}\n\n"
        f"📈 *Usage*\n"
        f"  Total commands: {stats['total_commands']}\n"
        f"  Today: {stats['today_commands']} cmds / {stats['today_unique_users']} users\n\n"
        f"🏆 *Top Commands*\n{top_cmds}\n\n"
        f"⏰ *Peak Hours (UTC)*: {peak_hrs}\n\n"
        f"🛡️ *Rate Limiting*\n"
        f"  Active bans: {abuse['active_bans']}\n"
        f"  Users warned: {abuse['users_with_warnings']}"
    )

    await update.message.reply_text(message, parse_mode='Markdown')


# =============================================================================
# SCHEDULED JOBS
# =============================================================================

async def admin_send_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin command to manually trigger the weekly summary broadcast."""
    user_id = update.effective_user.id
    if user_id not in ADMIN_USER_IDS:
        await update.message.reply_text("⛔ Not authorized.")
        return

    await update.message.reply_text("📤 Sending summary to all users...")
    await send_weekly_summary(context)
    user_ids = get_all_user_ids()
    await update.message.reply_text(f"✅ Summary sent to {len(user_ids)} users.")


async def send_weekly_summary(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send weekly Friday summary to all known users."""
    user_ids = get_all_user_ids()
    if not user_ids:
        logger.info("Weekly summary: no users to notify")
        return

    logger.info(f"Sending weekly summary to {len(user_ids)} users")

    regions = get_stations_by_region()

    for user_id in user_ids:
        try:
            message = "🎿 *Resum setmanal / Resumen semanal*\n\n"
            for region, stations in regions.items():
                message += f"🏔️ *{region}*\n"
                for sid, data in stations:
                    live_km, live_snow = get_conditions_display(sid)
                    km_open = live_km if live_km else data['km_open']
                    snow = live_snow if live_snow else data['snow']
                    message += f"  •  *{data['name']}*\n"
                    message += f"      📏 {km_open} | ❄️ {snow}\n"
                message += "\n"

            await context.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown',
            )
        except Exception as e:
            logger.warning(f"Could not send weekly summary to user {user_id}: {e}")
