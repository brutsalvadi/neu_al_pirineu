#!/usr/bin/env python3
"""
Simple script to plot bot analytics.

Usage:
    python plot_analytics.py           # Show all plots
    python plot_analytics.py --save    # Save plots to files
    python plot_analytics.py --summary # Just print summary
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from analytics import export_for_plotting, get_stats_summary


def print_summary() -> None:
    """Print a text summary of analytics."""
    stats = get_stats_summary()

    print("\n" + "=" * 50)
    print("📊 NORDIC SKI WEBCAMS BOT - ANALYTICS")
    print("=" * 50)

    print(f"\n👥 USERS")
    print(f"   Total users:        {stats['total_users']}")
    print(f"   Active (7 days):    {stats['active_users_7d']}")

    print(f"\n📈 USAGE")
    print(f"   Total commands:     {stats['total_commands']}")
    print(f"   Today's commands:   {stats['today_commands']}")
    print(f"   Today's users:      {stats['today_unique_users']}")

    print(f"\n🏆 TOP COMMANDS")
    for cmd, count in stats['top_commands'][:5]:
        print(f"   /{cmd}: {count}")

    print(f"\n⏰ PEAK HOURS (UTC)")
    for hour, count in stats['peak_hours']:
        print(f"   {hour}:00 - {count} commands")

    print("\n" + "=" * 50 + "\n")


def plot_analytics(save: bool = False) -> None:
    """Generate and display/save analytics plots."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime
    except ImportError:
        print("❌ matplotlib not installed. Install with: pip install matplotlib")
        print("   Showing text summary instead:\n")
        print_summary()
        return

    data = export_for_plotting()
    daily = data["daily"]
    growth = data["user_growth"]

    if not daily:
        print("📭 No data yet! Use the bot first to generate analytics.")
        return

    # Parse dates
    dates = [datetime.strptime(d["date"], "%Y-%m-%d") for d in daily]
    commands = [d["commands"] for d in daily]
    unique_users = [d["unique_users"] for d in daily]

    growth_dates = [datetime.strptime(d["date"], "%Y-%m-%d") for d in growth]
    total_users = [d["total_users"] for d in growth]

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Nordic Ski Webcams Bot - Analytics", fontsize=14, fontweight="bold")

    # Plot 1: Daily commands
    ax1 = axes[0, 0]
    ax1.bar(dates, commands, color="#1a472a", alpha=0.8)
    ax1.set_title("Daily Commands")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Commands")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates) // 10)))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Plot 2: Daily unique users
    ax2 = axes[0, 1]
    ax2.bar(dates, unique_users, color="#2196F3", alpha=0.8)
    ax2.set_title("Daily Unique Users")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Users")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates) // 10)))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Plot 3: User growth
    ax3 = axes[1, 0]
    if growth_dates:
        ax3.plot(growth_dates, total_users, marker="o", color="#4CAF50", linewidth=2)
        ax3.fill_between(growth_dates, total_users, alpha=0.3, color="#4CAF50")
    ax3.set_title("Cumulative User Growth")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Total Users")
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Plot 4: Hourly distribution
    ax4 = axes[1, 1]
    hourly = data["raw"].get("hourly_distribution", {})
    hours = [f"{h:02d}" for h in range(24)]
    hour_counts = [hourly.get(h, 0) for h in hours]
    ax4.bar(hours, hour_counts, color="#FF9800", alpha=0.8)
    ax4.set_title("Hourly Distribution (UTC)")
    ax4.set_xlabel("Hour")
    ax4.set_ylabel("Commands")

    plt.tight_layout()

    if save:
        output_path = Path(__file__).parent / "data" / "analytics_plot.png"
        output_path.parent.mkdir(exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"✅ Plot saved to: {output_path}")
    else:
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot bot analytics")
    parser.add_argument("--save", action="store_true", help="Save plots to file")
    parser.add_argument("--summary", action="store_true", help="Just print summary")
    args = parser.parse_args()

    if args.summary:
        print_summary()
    else:
        print_summary()
        plot_analytics(save=args.save)


if __name__ == "__main__":
    main()
