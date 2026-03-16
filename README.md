# Nordic Ski Webcams Telegram Bot

A Telegram bot that provides current conditions and webcam images from Nordic ski stations in the Pyrenees.

## Features

- Get current snow conditions (km open, snow depth)
- View live webcam images
- Supports 11 stations across 3 regions:
  - **Pirineo Catalán**: Aransa, Guils, Lles, Sant Joan, Tavascán, Tuixent, Virós
  - **Ariège Pyrénées**: Beille, Chioula
  - **Neiges Catalanes**: Capcir, Font-Romeu

## Commands

| Command | Aliases | Station |
|---------|---------|---------|
| `/aransa` | `/ara` | Aransa |
| `/guils` | `/gui` | Guils Fontanera |
| `/lles` | `/lle` | Lles de Cerdanya |
| `/santjoan` | `/sj`, `/erm` | Sant Joan de l'Erm |
| `/tavascan` | `/tav` | Tavascán |
| `/tuixent` | `/tui`, `/vansa` | Tuixent - La Vansa |
| `/viros` | `/vir` | Virós-Vallferrera |
| `/beille` | `/bei` | Beille |
| `/chioula` | `/chi` | Chioula |
| `/capcir` | `/cap` | Capcir |
| `/fontromeu` | `/fr`, `/font` | Font-Romeu Pyrénées 2000 |

Other commands:
- `/start` - Welcome message
- `/help` - Help and shortcuts
- `/list` - List all stations
- `/all` - Quick overview of all stations

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Choose a name (e.g., "Nordic Ski Webcams")
4. Choose a username (e.g., `nordic_ski_webcams_bot`)
5. Save the API token you receive (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Local Development (Polling Mode)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set token and run (polling mode - no WEBHOOK_URL)
export TELEGRAM_BOT_TOKEN="your_token_here"
python bot.py
```

The bot will run in **polling mode** locally (continuously asks Telegram for updates).

### 3. Deploy to a Server

The bot runs as a systemd service, deployed via rsync using the included `deploy.sh`.

```bash
# First-time setup: installs uv, syncs code, creates .env, registers systemd service
./deploy.sh --setup

# Set the bot token on the server
ssh pi@yourserver 'nano ~/src/neu_al_pirineu/.env'

# Start the service
ssh pi@yourserver 'sudo systemctl start nordic-ski-webcams'

# Subsequent deploys (sync code + restart service)
./deploy.sh
```

## Project Structure

```
├── bot.py              # Entry point: polling (local) or webhook mode
├── handlers.py         # Telegram command handlers
├── stations.py         # Station definitions (names, regions, webcam URLs, aliases)
├── data_sources.py     # Live data fetching (projecte4estacions, infonieve, capcir-nordique)
├── translations.py     # Multilingual string support
├── analytics.py        # Usage tracking
├── ratelimit.py        # Per-user rate limiting
├── utils.py            # Shared helpers
├── deploy.sh           # Deployment script (rsync + systemd)
├── deploy/
│   └── nordic-ski-webcams.service  # systemd service unit
└── pyproject.toml      # Python project and dependencies
```

## Updating Station Data

Station definitions (name, region, webcam URL, aliases) live in `stations.py`. Live conditions (km open, snow depth) are fetched at runtime by `data_sources.py` from infonieve.es, projecte4estacions.com, and capcir-nordique.com. Static fallback values in `stations.py` are used when live fetching fails.

To add or modify a station, edit the `STATIONS` dict in `stations.py` and redeploy with `fly deploy`.

## Webcam Sources

- **Catalan stations**: projecte4estacions.com
- **French stations**: bergfex.at

## Troubleshooting

### Check logs
```bash
ssh pi@yourserver 'journalctl -u nordic-ski-webcams -f'
```

### Restart the service
```bash
ssh pi@yourserver 'sudo systemctl restart nordic-ski-webcams'
```

### Check service status
```bash
ssh pi@yourserver 'sudo systemctl status nordic-ski-webcams'
```

## License

MIT
