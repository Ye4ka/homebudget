#!/bin/bash
# Complete backup system for HomeBudget PostgreSQL database
# Использует пользователя myuser
# Usage: ./scripts/backup.sh [--daily|--weekly|--monthly]

set -e  # Exit on error

echo "HOME BUDGET DATABASE BACKUP SYSTEM"
echo "======================================"

# Configuration
BACKUP_ROOT="${BACKUP_ROOT:-$(pwd)/backups}"
DB_NAME="${DB_NAME:-homebudget}"
DB_USER="${DB_USER:-myuser}"  # Явно указываем пользователя
BACKUP_TYPE="${1:---daily}"  # --daily, --weekly, --monthly

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load database configuration
if [ -f ".env" ]; then
    echo "Loading database configuration from .env file..."
    # Ищем параметры в .env
    if grep -q "POSTGRES_DB" .env; then
        DB_NAME=$(grep POSTGRES_DB .env | cut -d '=' -f2-)
    fi
    if grep -q "POSTGRES_USER" .env; then
        DB_USER=$(grep POSTGRES_USER .env | cut -d '=' -f2-)
    fi
    if grep -q "POSTGRES_PASSWORD" .env; then
        export PGPASSWORD=$(grep POSTGRES_PASSWORD .env | cut -d '=' -f2-)
    fi
fi

# Проверяем, установлен ли пароль
if [ -z "$PGPASSWORD" ]; then
    echo -e "${YELLOW}Warning: PGPASSWORD not set. Trying without password...${NC}"
fi

# Формируем строку подключения для psql/pg_dump
DB_CONNECTION="-h localhost -p 5432 -U $DB_USER -d $DB_NAME"

# Set backup directory based on type
case $BACKUP_TYPE in
    "--daily")
        BACKUP_DIR="$BACKUP_ROOT/daily"
        ROTATION_DAYS=7
        ;;
    "--weekly")
        BACKUP_DIR="$BACKUP_ROOT/weekly"
        ROTATION_DAYS=30
        ;;
    "--monthly")
        BACKUP_DIR="$BACKUP_ROOT/monthly"
        ROTATION_DAYS=365
        ;;
    *)
        echo -e "${YELLOW}Unknown backup type. Using daily.${NC}"
        BACKUP_DIR="$BACKUP_ROOT/daily"
        ROTATION_DAYS=7
        ;;
esac

# Create backup directory
mkdir -p "$BACKUP_DIR"
mkdir -p "$BACKUP_ROOT/logs"

# Timestamp for filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_${TIMESTAMP}.sql.gz"
LOG_FILE="$BACKUP_ROOT/logs/backup_${TIMESTAMP}.log"

echo -e "${BLUE}BACKUP CONFIGURATION${NC}"
echo "Database:      $DB_NAME"
echo "User:          $DB_USER"
echo "Backup type:   $BACKUP_TYPE"
echo "Backup dir:    $BACKUP_DIR"
echo "Rotation:      $ROTATION_DAYS days"
echo "Backup file:   $(basename $BACKUP_FILE)"
echo "Log file:      $(basename $LOG_FILE)"

# Test database connection
echo -e "\n${BLUE}TESTING DATABASE CONNECTION${NC}"
if ! psql $DB_CONNECTION -c "SELECT NOW();" > /dev/null 2>&1; then
    echo -e "${RED} Cannot connect to database${NC}"
    echo "Connection string: psql $DB_CONNECTION"
    echo "Make sure PostgreSQL is running and user '$DB_USER' has access"
    
    # Попробуем подключиться с помощью sudo
    echo -e "\n${YELLOW} Trying sudo connection to postgres user...${NC}"
    if sudo -u postgres psql -c "SELECT NOW();" > /dev/null 2>&1; then
        echo -e "${GREEN} Can connect as postgres user${NC}"
    fi
    
    exit 1
fi
echo -e "${GREEN}Database connection successful${NC}"

# Get database size
echo -e "\n${BLUE}DATABASE STATISTICS${NC}"
DB_SIZE=$(psql $DB_CONNECTION -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));" | tr -d ' ')
TABLE_COUNT=$(psql $DB_CONNECTION -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
echo "Database size: $DB_SIZE"
echo "Tables count:  $TABLE_COUNT"

# Create backup
echo -e "\n${BLUE}CREATING BACKUP${NC}"
echo "Start time: $(date '+%Y-%m-%d %H:%M:%S')"

START_TIME=$(date +%s)

# Create backup with pg_dump
echo "Running pg_dump..."
pg_dump $DB_CONNECTION \
    --format=custom \
    --no-owner \
    --no-acl \
    --clean \
    --if-exists \
    --verbose 2>&1 | tee -a "$LOG_FILE" | gzip > "$BACKUP_FILE"

BACKUP_RESULT=$?
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ $BACKUP_RESULT -eq 0 ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo -e "${GREEN}Backup created successfully!${NC}"
    echo "Backup size:  $BACKUP_SIZE"
    echo "Duration:     ${DURATION}s"
else
    echo -e "${RED}Backup failed with code $BACKUP_RESULT${NC}"
    echo "Check log file: $LOG_FILE"
    exit 1
fi

# Verify backup
echo -e "\n${BLUE}VERIFYING BACKUP${NC}"
if gunzip -t "$BACKUP_FILE" 2>/dev/null; then
    echo -e "${GREEN}Backup file is valid (gzip test)${NC}"
else
    echo -e "${RED}Backup file is corrupted!${NC}"
    exit 1
fi

# Old backups rotation
echo -e "\n${BLUE}🗑️  ROTATING OLD BACKUPS${NC}"
OLD_BACKUPS_COUNT=$(find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$ROTATION_DAYS | wc -l)

if [ $OLD_BACKUPS_COUNT -gt 0 ]; then
    echo "Found $OLD_BACKUPS_COUNT backups older than $ROTATION_DAYS days"
    find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$ROTATION_DAYS -print0 | while IFS= read -r -d $'\0' old_backup; do
        echo "  Deleting: $(basename "$old_backup")"
        rm "$old_backup"
    done
    echo -e "${GREEN}Old backups cleaned up${NC}"
else
    echo "No old backups to clean up"
fi

# Backup statistics
echo -e "\n${BLUE}BACKUP STATISTICS${NC}"
TOTAL_BACKUPS=$(find "$BACKUP_DIR" -name "*.sql.gz" | wc -l)
TOTAL_SIZE=$(find "$BACKUP_DIR" -name "*.sql.gz" -exec du -ch {} + | grep total | cut -f1)

echo "Total backups in $BACKUP_DIR: $TOTAL_BACKUPS"
echo "Total size: $TOTAL_SIZE"

# List recent backups
echo -e "\n${BLUE}RECENT BACKUPS${NC}"
find "$BACKUP_DIR" -name "*.sql.gz" -type f -printf "%T@ %p\n" | sort -nr | head -5 | while read -r line; do
    timestamp=$(echo "$line" | cut -d' ' -f1)
    filepath=$(echo "$line" | cut -d' ' -f2-)
    filename=$(basename "$filepath")
    size=$(du -h "$filepath" | cut -f1)
    date_str=$(date -d "@$timestamp" '+%Y-%m-%d %H:%M')
    echo "  $date_str - $filename ($size)"
done

# Create summary report
SUMMARY_FILE="$BACKUP_ROOT/last_backup.summary"
cat > "$SUMMARY_FILE" << EOF
BACKUP SUMMARY
==============
Date:          $(date '+%Y-%m-%d %H:%M:%S')
Type:          $BACKUP_TYPE
Database:      $DB_NAME
User:          $DB_USER
Backup file:   $(basename "$BACKUP_FILE")
Backup size:   $BACKUP_SIZE
Duration:      ${DURATION}s
Status:        SUCCESS
Total backups: $TOTAL_BACKUPS
Total size:    $TOTAL_SIZE
EOF

echo -e "\n${GREEN}BACKUP COMPLETED SUCCESSFULLY!${NC}"
echo "Summary saved to: $SUMMARY_FILE"
echo "Log file: $LOG_FILE"

# Clean up password from environment
unset PGPASSWORD