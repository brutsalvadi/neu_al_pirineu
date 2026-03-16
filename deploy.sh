#!/usr/bin/env bash
#
# Deploy the Nordic Ski Webcams bot to your server
#
# Usage:
#   ./deploy.sh          # Sync code and restart the bot
#   ./deploy.sh --setup  # First-time setup (installs uv, systemd service, .env)
#

set -euo pipefail

REMOTE="user@yourserver.local"
REMOTE_DIR="/home/user/src/neu_al_pirineu"
LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_NAME="nordic-ski-webcams"

# PATH prefix for non-interactive SSH (uv installs to ~/.local/bin)
REMOTE_PATH="export PATH=\$HOME/.local/bin:\$PATH"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}==>${NC} $1"; }
warn() { echo -e "${YELLOW}==>${NC} $1"; }

# ─── First-time setup ────────────────────────────────────────────────────────
setup() {
    log "Initial setup on ${REMOTE}..."

    # Create directory
    ssh "$REMOTE" "mkdir -p ${REMOTE_DIR}"

    # Install uv if not present
    log "Checking uv..."
    ssh "$REMOTE" "${REMOTE_PATH} && command -v uv >/dev/null 2>&1 || { echo 'Installing uv...'; curl -LsSf https://astral.sh/uv/install.sh | sh; }"

    # Sync code
    do_sync

    # Create .env if not present
    ssh "$REMOTE" "test -f ${REMOTE_DIR}/.env || { echo 'TELEGRAM_BOT_TOKEN=INSERT_TOKEN_HERE' > ${REMOTE_DIR}/.env; echo 'Created .env - SET YOUR TOKEN!'; }"

    # Install dependencies
    log "Installing Python dependencies..."
    ssh "$REMOTE" "${REMOTE_PATH} && cd ${REMOTE_DIR} && uv sync"

    # Install systemd service
    log "Installing systemd service..."
    ssh "$REMOTE" "sudo cp ${REMOTE_DIR}/deploy/${SERVICE_NAME}.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable ${SERVICE_NAME}"

    log "Setup complete!"
    warn "Remember to:"
    warn "  1. Set the token: ssh ${REMOTE} 'nano ${REMOTE_DIR}/.env'"
    warn "  2. Start the bot: ssh ${REMOTE} 'sudo systemctl start ${SERVICE_NAME}'"
    warn ""
    warn "Then just use: ./deploy.sh"
}

# ─── File sync ───────────────────────────────────────────────────────────────
do_sync() {
    log "Syncing code..."
    rsync -avz --delete \
        --exclude '.venv/' \
        --exclude 'venv/' \
        --exclude '__pycache__/' \
        --exclude '.env' \
        --exclude 'data/' \
        --exclude '.git/' \
        --exclude '*.pyc' \
        --exclude '*.egg-info/' \
        "${LOCAL_DIR}/" "${REMOTE}:${REMOTE_DIR}/"
}

# ─── Standard deploy ─────────────────────────────────────────────────────────
deploy() {
    do_sync

    log "Restarting bot..."
    ssh "$REMOTE" "${REMOTE_PATH} && cd ${REMOTE_DIR} && uv sync --quiet && sudo systemctl restart ${SERVICE_NAME}"

    sleep 2
    log "Service status:"
    ssh "$REMOTE" "sudo systemctl status ${SERVICE_NAME} --no-pager -l" || true

    log "Deploy complete!"
}

# ─── Main ────────────────────────────────────────────────────────────────────
case "${1:-}" in
    --setup)
        setup
        ;;
    *)
        deploy
        ;;
esac
