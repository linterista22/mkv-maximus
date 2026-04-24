#!/bin/bash
# Build and start MKV Maximus Docker container.
# Run from the project root: sudo bash deploy.sh
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# First-run: create .env if missing
if [ ! -f "$PROJECT_DIR/.env" ]; then
  echo ""
  echo "==> First run: .env not found."
  echo "    Enter the path to your media folder (e.g. /media/youruser/HDD):"
  read -r media_path
  echo "MEDIA_PATH=$media_path" > "$PROJECT_DIR/.env"
  echo "==> .env created. This file is not tracked by git — your path is safe across updates."
  echo ""
fi

echo "==> Building and starting container..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" up --build -d

echo "==> Done. App available at http://$(hostname -I | awk '{print $1}'):7788/"
