"""
Rate limiting and abuse protection for the Nordic Ski Webcams Telegram Bot.

Features:
- Per-user rate limiting (commands per minute/hour)
- Cooldown between commands
- Automatic temporary bans for excessive usage
- Permanent ban list for persistent abusers
"""

import time
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# =============================================================================
# CONFIGURATION
# =============================================================================

# Rate limits
MAX_COMMANDS_PER_MINUTE = 10  # Max commands per user per minute
MAX_COMMANDS_PER_HOUR = 60    # Max commands per user per hour
MIN_COMMAND_INTERVAL = 1.0    # Minimum seconds between commands (cooldown)

# Ban thresholds
WARNINGS_BEFORE_TEMP_BAN = 3  # Warnings before temporary ban
TEMP_BAN_DURATION = 300       # Temporary ban duration in seconds (5 minutes)
TEMP_BANS_BEFORE_LONG_BAN = 3 # Temp bans before longer ban
LONG_BAN_DURATION = 3600      # Long ban duration in seconds (1 hour)

# Admin user IDs (can bypass rate limits) - set via environment or config
ADMIN_USER_IDS: set[int] = set()


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class UserRateData:
    """Track rate limiting data for a single user."""
    command_timestamps: list[float] = field(default_factory=list)
    last_command_time: float = 0.0
    warnings: int = 0
    temp_ban_count: int = 0
    banned_until: float = 0.0
    is_permanently_banned: bool = False


# In-memory storage (in production, use Redis or similar)
_user_data: dict[int, UserRateData] = defaultdict(UserRateData)
_permanent_bans: set[int] = set()


# =============================================================================
# RATE LIMITING FUNCTIONS
# =============================================================================

def _cleanup_old_timestamps(data: UserRateData, now: float) -> None:
    """Remove timestamps older than 1 hour."""
    one_hour_ago = now - 3600
    data.command_timestamps = [ts for ts in data.command_timestamps if ts > one_hour_ago]


def _count_recent_commands(data: UserRateData, now: float, seconds: int) -> int:
    """Count commands in the last N seconds."""
    cutoff = now - seconds
    return sum(1 for ts in data.command_timestamps if ts > cutoff)


def is_user_banned(user_id: int) -> bool:
    """Check if a user is currently banned."""
    if user_id in _permanent_bans:
        return True

    data = _user_data[user_id]
    if data.is_permanently_banned:
        return True

    now = time.time()
    if data.banned_until > now:
        return True

    return False


def get_ban_remaining(user_id: int) -> int:
    """Get remaining ban time in seconds (0 if not banned)."""
    if user_id in _permanent_bans or _user_data[user_id].is_permanently_banned:
        return -1  # -1 indicates permanent ban

    data = _user_data[user_id]
    now = time.time()
    if data.banned_until > now:
        return int(data.banned_until - now)
    return 0


def check_rate_limit(user_id: int) -> tuple[bool, str]:
    """
    Check if a user can execute a command.

    Returns:
        Tuple of (allowed: bool, message: str)
        - If allowed, message is empty
        - If not allowed, message explains why
    """
    # Admins bypass rate limits
    if user_id in ADMIN_USER_IDS:
        return True, ""

    now = time.time()
    data = _user_data[user_id]

    # Check permanent ban
    if data.is_permanently_banned or user_id in _permanent_bans:
        logger.warning(f"Blocked permanently banned user {user_id}")
        return False, "🚫 You have been permanently banned for abuse."

    # Check temporary ban
    if data.banned_until > now:
        remaining = int(data.banned_until - now)
        logger.info(f"Blocked temp-banned user {user_id}, {remaining}s remaining")
        return False, f"⏳ You are temporarily banned. Try again in {remaining} seconds."

    # Cleanup old timestamps
    _cleanup_old_timestamps(data, now)

    # Check cooldown (minimum interval between commands)
    time_since_last = now - data.last_command_time
    if time_since_last < MIN_COMMAND_INTERVAL:
        return False, "⏱️ Please wait a moment before sending another command."

    # Check per-minute limit
    commands_last_minute = _count_recent_commands(data, now, 60)
    if commands_last_minute >= MAX_COMMANDS_PER_MINUTE:
        data.warnings += 1
        logger.warning(f"User {user_id} exceeded per-minute limit ({commands_last_minute} cmds), warning {data.warnings}")

        if data.warnings >= WARNINGS_BEFORE_TEMP_BAN:
            _apply_temp_ban(user_id, data, now)
            return False, f"🚫 Too many requests. You have been temporarily banned for {TEMP_BAN_DURATION // 60} minutes."

        return False, f"⚠️ Slow down! Max {MAX_COMMANDS_PER_MINUTE} commands per minute. Warning {data.warnings}/{WARNINGS_BEFORE_TEMP_BAN}."

    # Check per-hour limit
    commands_last_hour = _count_recent_commands(data, now, 3600)
    if commands_last_hour >= MAX_COMMANDS_PER_HOUR:
        data.warnings += 1
        logger.warning(f"User {user_id} exceeded per-hour limit ({commands_last_hour} cmds), warning {data.warnings}")

        if data.warnings >= WARNINGS_BEFORE_TEMP_BAN:
            _apply_temp_ban(user_id, data, now)
            return False, f"🚫 Too many requests this hour. You have been temporarily banned for {TEMP_BAN_DURATION // 60} minutes."

        return False, f"⚠️ You've reached the hourly limit ({MAX_COMMANDS_PER_HOUR} commands). Warning {data.warnings}/{WARNINGS_BEFORE_TEMP_BAN}."

    return True, ""


def record_command(user_id: int) -> None:
    """Record that a user executed a command."""
    now = time.time()
    data = _user_data[user_id]
    data.command_timestamps.append(now)
    data.last_command_time = now


def _apply_temp_ban(user_id: int, data: UserRateData, now: float) -> None:
    """Apply a temporary ban to a user."""
    data.temp_ban_count += 1
    data.warnings = 0  # Reset warnings after ban

    if data.temp_ban_count >= TEMP_BANS_BEFORE_LONG_BAN:
        # Apply longer ban
        data.banned_until = now + LONG_BAN_DURATION
        logger.warning(f"User {user_id} received LONG ban ({LONG_BAN_DURATION}s) - temp ban count: {data.temp_ban_count}")
    else:
        data.banned_until = now + TEMP_BAN_DURATION
        logger.warning(f"User {user_id} received temp ban ({TEMP_BAN_DURATION}s) - temp ban count: {data.temp_ban_count}")


# =============================================================================
# ADMIN FUNCTIONS
# =============================================================================

def add_admin(user_id: int) -> None:
    """Add a user to the admin list."""
    ADMIN_USER_IDS.add(user_id)
    logger.info(f"Added admin: {user_id}")


def remove_admin(user_id: int) -> None:
    """Remove a user from the admin list."""
    ADMIN_USER_IDS.discard(user_id)
    logger.info(f"Removed admin: {user_id}")


def ban_user(user_id: int, permanent: bool = False) -> None:
    """Ban a user."""
    if permanent:
        _permanent_bans.add(user_id)
        _user_data[user_id].is_permanently_banned = True
        logger.warning(f"Permanently banned user: {user_id}")
    else:
        _user_data[user_id].banned_until = time.time() + LONG_BAN_DURATION
        logger.warning(f"Banned user {user_id} for {LONG_BAN_DURATION}s")


def unban_user(user_id: int) -> None:
    """Unban a user."""
    _permanent_bans.discard(user_id)
    data = _user_data[user_id]
    data.is_permanently_banned = False
    data.banned_until = 0
    data.warnings = 0
    data.temp_ban_count = 0
    logger.info(f"Unbanned user: {user_id}")


def get_user_status(user_id: int) -> dict[str, Any]:
    """Get rate limit status for a user."""
    data = _user_data[user_id]
    now = time.time()
    _cleanup_old_timestamps(data, now)

    return {
        "user_id": user_id,
        "is_admin": user_id in ADMIN_USER_IDS,
        "is_banned": is_user_banned(user_id),
        "ban_remaining": get_ban_remaining(user_id),
        "warnings": data.warnings,
        "temp_ban_count": data.temp_ban_count,
        "commands_last_minute": _count_recent_commands(data, now, 60),
        "commands_last_hour": _count_recent_commands(data, now, 3600),
    }


def get_abuse_summary() -> dict[str, Any]:
    """Get summary of rate limiting activity."""
    now = time.time()

    active_bans = 0
    users_with_warnings = 0
    total_tracked_users = len(_user_data)

    for user_id, data in _user_data.items():
        if is_user_banned(user_id):
            active_bans += 1
        if data.warnings > 0:
            users_with_warnings += 1

    return {
        "total_tracked_users": total_tracked_users,
        "active_bans": active_bans,
        "permanent_bans": len(_permanent_bans),
        "users_with_warnings": users_with_warnings,
        "admin_count": len(ADMIN_USER_IDS),
    }
