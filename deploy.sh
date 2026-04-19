#!/bin/bash
# Build and start MKV Maximus Docker container.
# Run from the project root: sudo bash deploy.sh
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Building and starting container..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" up --build -d

echo "==> Done. App available at http://$(hostname -I | awk '{print $1}'):7788/"
