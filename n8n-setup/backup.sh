#!/bin/bash

# N8N Backup Script
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🔄 Starting N8N backup..."

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup N8N data
docker-compose exec -T n8n n8n export:workflow --backup --output=/tmp/workflows_$DATE.json
docker cp n8n-resort:/tmp/workflows_$DATE.json "$BACKUP_DIR/"

# Backup database
docker-compose exec -T postgres pg_dump -U n8n n8n > "$BACKUP_DIR/database_$DATE.sql"

# Backup credentials (encrypted)
docker cp n8n-resort:/home/node/.n8n/credentials.json "$BACKUP_DIR/credentials_$DATE.json" 2>/dev/null || echo "No credentials to backup"

# Compress backup
tar -czf "$BACKUP_DIR/n8n_backup_$DATE.tar.gz" -C "$BACKUP_DIR" workflows_$DATE.json database_$DATE.sql credentials_$DATE.json 2>/dev/null

# Clean up individual files
rm -f "$BACKUP_DIR/workflows_$DATE.json" "$BACKUP_DIR/database_$DATE.sql" "$BACKUP_DIR/credentials_$DATE.json"

echo "✅ Backup completed: n8n_backup_$DATE.tar.gz"

# Keep only last 7 backups
find "$BACKUP_DIR" -name "n8n_backup_*.tar.gz" -type f -mtime +7 -delete
