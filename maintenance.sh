#!/bin/bash
# Backup and Monitoring script for Gold Tracker
# Uses 'claw-backup' (local mode) and 'system-resource-monitor'

# Configuration
BACKUP_DIR="/home/mus/backups/gold-tracker"
DB_NAME="goldtracker"
DB_USER="goldtracker"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql.gz"

# 1. Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# 2. Run Database Backup
echo "--- Starting PostgreSQL Backup ---"
docker exec gold-tracker-db pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_FILE"
    # Keep only last 30 days of database backups
    find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +30 -delete
else
    echo "Backup FAILED"
    exit 1
fi

# 3. Trigger OpenClaw Files Backup (using installed claw-backup skill structure)
# Note: Since setup.js usually handles the full config, we'll manually archive 
# the production folder as part of this maintenance script.
echo "--- Backing up Production Files ---"
tar -czf "${BACKUP_DIR}/prod_files_${TIMESTAMP}.tar.gz" /home/mus/production/gold-tracker-dz --exclude="node_modules" --exclude="venv"

# 4. System Health Check
echo "--- System Health Report ---"
bash /home/mus/.openclaw/workspace/skills/system-resource-monitor/scripts/monitor.sh

echo "Maintenance cycle complete."
