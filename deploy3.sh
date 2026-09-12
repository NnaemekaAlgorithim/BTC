#!/bin/bash
# deploy3.sh
#
# Run this on your server whenever you want to deploy a new version of BTC.
#
# Usage:
#   chmod +x deploy3.sh
#   ./deploy3.sh
#
# What it does:
#   1. Pulls latest code from Git
#   2. Rebuilds Docker images (web + migrate)
#   3. Runs migrations
#   4. Restarts the web service
#   5. Cleans up old images to save disk space
#
# Note: this project shares InventoryMaster2's nginx container over the
# "shared_frontend" docker network, so InventoryMaster2's stack must already
# be running before the first deploy (that's what creates the network).

set -euo pipefail

REPO_URL="https://github.com/NnaemekaAlgorithim/BTC.git"
BRANCH="main"
PROJECT_DIR="/root/BTC"

echo "=============================="
echo "       BTC Deployment         "
echo "=============================="

# ── Step 1: Pull latest code ──────────────────────────────────────────────────
echo ""
echo "[1/5] Pulling latest code from Git..."
cd "$PROJECT_DIR"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"
echo "Code updated."

# ── Step 2: Build new Docker images ──────────────────────────────────────────
echo ""
echo "[2/5] Building Docker images..."
docker compose build web migrate
echo "Images built."

# ── Step 3: Run migrations (one-shot container) ────────────────────────────────
echo ""
echo "[3/5] Running database migrations..."
docker compose run --rm migrate
echo "Migrations complete."

# ── Step 4: Restart web service ──────────────────────────────────────────────
echo ""
echo "[4/5] Restarting web service..."
docker compose up -d --no-deps --force-recreate --remove-orphans web
echo "Service restarted."

# ── Step 5: Clean up old images ───────────────────────────────────────────────
echo ""
echo "[5/5] Cleaning up unused Docker images..."
docker image prune -f
echo "Cleanup done."

# ── Verify everything is running ──────────────────────────────────────────────
echo ""
echo "Service status:"
docker compose ps

echo ""
echo "=============================="
echo " Deployment complete!         "
echo "=============================="
echo ""
echo "Check logs with:"
echo "  docker compose logs -f web"
