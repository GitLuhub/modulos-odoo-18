#!/bin/bash

set -e

BACKUP_DIR="${BACKUP_DIR:-./backups}"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="${DB_NAME:-odoo}"
DB_USER="${DB_USER:-odoo}"
DB_HOST="${DB_HOST:-localhost}"

mkdir -p "$BACKUP_DIR"

echo "Starting backup..."

pg_dump -h "$DB_HOST" -U "$DB_USER" -Fc "$DB_NAME" > "$BACKUP_DIR/${DB_NAME}_${DATE}.dump"

echo "Backup created: $BACKUP_DIR/${DB_NAME}_${DATE}.dump"

find "$BACKUP_DIR" -type f -name "*.dump" -mtime +7 -delete

echo "Old backups (older than 7 days) cleaned up"
echo "Backup completed successfully!"
