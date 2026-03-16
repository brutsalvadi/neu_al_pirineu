"""
Simple analytics and logging for the Nordic Ski Webcams Telegram Bot.

Tracks:
- Unique users
- Command usage over time
- Daily/hourly activity patterns

Data is stored in a simple JSON file for easy access and plotting.
"""

import json
import os
import logging
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict
from typing import Any

logger = logging.getLogger(__name__)

# Analytics data file path
ANALYTICS_DIR = Path(__file__).parent / "data"
ANALYTICS_FILE = ANALYTICS_DIR / "analytics.json"


def _ensure_data_dir() -> None:
    """Ensure the data directory exists."""
    ANALYTICS_DIR.mkdir(exist_ok=True)


def _load_analytics() -> dict[str, Any]:
    """Load analytics data from file."""
    _ensure_data_dir()
    if ANALYTICS_FILE.exists():
        try:
            with open(ANALYTICS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading analytics: {e}")

    # Return default structure
    return {
        "users": {},  # user_id -> {first_seen, last_seen, username, command_count}
        "daily_stats": {},  # "YYYY-MM-DD" -> {commands: int, unique_users: []}
        "command_counts": {},  # command_name -> count
        "hourly_distribution": {},  # "HH" -> count
    }


def _save_analytics(data: dict[str, Any]) -> None:
    """Save analytics data to file."""
    _ensure_data_dir()
    try:
        with open(ANALYTICS_FILE, "w") as f:
            json.dump(data, f, indent=2, default=str)
    except IOError as e:
        logger.error(f"Error saving analytics: {e}")


def log_command(user_id: int, username: str | None, command: str) -> None:
    """
    Log a command execution.

    Args:
        user_id: Telegram user ID
        username: Telegram username (may be None)
        command: The command that was executed
    """
    data = _load_analytics()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H")
    user_id_str = str(user_id)

    # Update user info
    if user_id_str not in data["users"]:
        data["users"][user_id_str] = {
            "first_seen": now.isoformat(),
            "last_seen": now.isoformat(),
            "username": username,
            "command_count": 0,
        }

    data["users"][user_id_str]["last_seen"] = now.isoformat()
    data["users"][user_id_str]["command_count"] += 1
    if username:
        data["users"][user_id_str]["username"] = username

    # Update daily stats
    if today not in data["daily_stats"]:
        data["daily_stats"][today] = {
            "commands": 0,
            "unique_users": [],
        }

    data["daily_stats"][today]["commands"] += 1
    if user_id_str not in data["daily_stats"][today]["unique_users"]:
        data["daily_stats"][today]["unique_users"].append(user_id_str)

    # Update command counts
    if command not in data["command_counts"]:
        data["command_counts"][command] = 0
    data["command_counts"][command] += 1

    # Update hourly distribution
    if hour not in data["hourly_distribution"]:
        data["hourly_distribution"][hour] = 0
    data["hourly_distribution"][hour] += 1

    _save_analytics(data)


def get_stats_summary() -> dict[str, Any]:
    """
    Get a summary of analytics data.

    Returns:
        Dictionary with summary statistics
    """
    data = _load_analytics()

    total_users = len(data["users"])
    total_commands = sum(data["command_counts"].values())

    # Users active in last 7 days
    now = datetime.now()
    active_7d = 0
    for user_info in data["users"].values():
        last_seen = datetime.fromisoformat(user_info["last_seen"])
        if (now - last_seen).days <= 7:
            active_7d += 1

    # Today's stats
    today = now.strftime("%Y-%m-%d")
    today_stats = data["daily_stats"].get(today, {"commands": 0, "unique_users": []})

    # Most popular commands
    top_commands = sorted(
        data["command_counts"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    # Peak hours
    peak_hours = sorted(
        data["hourly_distribution"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    return {
        "total_users": total_users,
        "active_users_7d": active_7d,
        "total_commands": total_commands,
        "today_commands": today_stats["commands"],
        "today_unique_users": len(today_stats["unique_users"]),
        "top_commands": top_commands,
        "peak_hours": peak_hours,
    }


def get_daily_data() -> list[dict[str, Any]]:
    """
    Get daily statistics for plotting.

    Returns:
        List of daily stats sorted by date
    """
    data = _load_analytics()

    daily_list = []
    for date_str, stats in sorted(data["daily_stats"].items()):
        daily_list.append({
            "date": date_str,
            "commands": stats["commands"],
            "unique_users": len(stats["unique_users"]),
        })

    return daily_list


def get_user_growth() -> list[dict[str, Any]]:
    """
    Get cumulative user growth over time.

    Returns:
        List of {date, total_users} sorted by date
    """
    data = _load_analytics()

    # Get first seen dates for all users
    first_seen_dates = defaultdict(int)
    for user_info in data["users"].values():
        first_seen = datetime.fromisoformat(user_info["first_seen"]).strftime("%Y-%m-%d")
        first_seen_dates[first_seen] += 1

    # Calculate cumulative growth
    growth = []
    cumulative = 0
    for date_str in sorted(first_seen_dates.keys()):
        cumulative += first_seen_dates[date_str]
        growth.append({
            "date": date_str,
            "total_users": cumulative,
            "new_users": first_seen_dates[date_str],
        })

    return growth


def get_all_user_ids() -> list[int]:
    """Return all known user IDs."""
    data = _load_analytics()
    return [int(uid) for uid in data["users"].keys()]


def export_for_plotting() -> dict[str, Any]:
    """
    Export all data in a format suitable for plotting.

    Returns:
        Dictionary with all plotting data
    """
    return {
        "summary": get_stats_summary(),
        "daily": get_daily_data(),
        "user_growth": get_user_growth(),
        "raw": _load_analytics(),
    }
