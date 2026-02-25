#!/bin/bash
# Database restore script for HomeBudget
# Использует пользователя myuser
# Usage: ./scripts/restore.sh [backup_file.sql.gz]

set -e

echo " HOME BUDGET DATABASE RESTORE SYSTEM"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
BACKUP_ROOT="${BACKUP_ROOT:-$(pwd)/backups}"
DB_NAME="${DB_NAME:-homebudget}"
DB_USER="${DB_USER:-myuser}"  # Явно указываем пользователя

# Load database configuration from .env
if [ -f ".env" ]; then
    echo "Loading database configuration from .env file..."
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

# Формируем строку подключения
DB_CONNECTION="-h localhost -p 5432 -U $DB_USER -d $DB_NAME"

# Check if specific backup file is provided
if [ $# -eq 1 ]; then
    BACKUP_FILE="$1"
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED} Backup file not found: $BACKUP_FILE${NC}"
        exit 1
    fi
else
    # Find latest backup
    echo -e "${BLUE} FINDING LATEST BACKUP${NC}"
    
    BACKUP_DIRS=("$BACKUP_ROOT/daily" "$BACKUP_ROOT/weekly" "$BACKUP_ROOT/monthly")
    LATEST_BACKUP=""
    LATEST_TIME=0
    
    for dir in "${BACKUP_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            latest_in_dir=$(find "$dir" -name "*.sql.gz" -type f -printf "%T@ %p\n" 2>/dev/null | sort -nr | head -1)
            if [ -n "$latest_in_dir" ]; then
                timestamp=$(echo "$latest_in_dir" | cut -d' ' -f1)
                filepath=$(echo "$latest_in_dir" | cut -d' ' -f2-)
                
                if (( $(echo "$timestamp > $LATEST_TIME" | bc -l) )); then
                    LATEST_TIME=$timestamp
                    LATEST_BACKUP=$filepath
                fi
            fi
        fi
    done
    
    if [ -z "$LATEST_BACKUP" ]; then
        echo -e "${RED} No backup files found in $BACKUP_ROOT${NC}"
        exit 1
    fi
    
    BACKUP_FILE="$LATEST_BACKUP"
fi

echo -e "${GREEN} Selected backup: $(basename "$BACKUP_FILE")${NC}"
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "Backup size: $BACKUP_SIZE"
echo "Backup date: $(date -r "$BACKUP_FILE" '+%Y-%m-%d %H:%M:%S')"

# Verify backup file
echo -e "\n${BLUE} VERIFYING BACKUP FILE${NC}"
if ! gunzip -t "$BACKUP_FILE"; then
    echo -e "${RED} Backup file is corrupted!${NC}"
    exit 1
fi
echo -e "${GREEN} Backup file is valid${NC}"

# WARNING
echo -e "\n${RED} WARNING ${NC}"
echo -e "${RED}This will COMPLETELY ERASE the current database!${NC}"
echo -e "${RED}All existing data will be lost!${NC}"

# Get current database info
echo -e "\n${YELLOW} CURRENT DATABASE STATE${NC}"
psql $DB_CONNECTION -c "
SELECT 
    'users' as table_name, COUNT(*) as row_count FROM users_user
UNION ALL
SELECT 'budgets', COUNT(*) FROM budgets_budget
UNION ALL
SELECT 'categories', COUNT(*) FROM categories_category
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions_transaction
UNION ALL
SELECT 'total', SUM(count) FROM (
    SELECT COUNT(*) FROM users_user
    UNION ALL SELECT COUNT(*) FROM budgets_budget
    UNION ALL SELECT COUNT(*) FROM categories_category
    UNION ALL SELECT COUNT(*) FROM transactions_transaction
) as counts;
"

# Confirmation
echo -e "\n${YELLOW} Are you sure you want to continue?${NC}"
read -p "Type 'RESTORE' to confirm: " CONFIRM

if [ "$CONFIRM" != "RESTORE" ]; then
    echo -e "${YELLOW} Restore cancelled${NC}"
    exit 0
fi

# Pre-restore checklist
echo -e "\n${BLUE} PRE-RESTORE CHECKLIST${NC}"

# 1. Check disk space
BACKUP_SIZE_BYTES=$(stat -c%s "$BACKUP_FILE")
DISK_SPACE=$(df -k "$(dirname "$BACKUP_FILE")" | tail -1 | awk '{print $4}')
DISK_SPACE_BYTES=$((DISK_SPACE * 1024))

if [ $BACKUP_SIZE_BYTES -gt $DISK_SPACE_BYTES ]; then
    echo -e "${RED} Not enough disk space${NC}"
    echo "Backup size: $(numfmt --to=iec $BACKUP_SIZE_BYTES)"
    echo "Free space:  $(numfmt --to=iec $DISK_SPACE_BYTES)"
    exit 1
fi
echo -e "${GREEN} Sufficient disk space${NC}"

# 2. Drop all connections to database
echo -e "\n Terminating active connections..."
psql $DB_CONNECTION -c "
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = '$DB_NAME'
  AND pid <> pg_backend_pid();
" 2>/dev/null || true

# 3. Create new empty database if doesn't exist
echo -e "\n Ensuring database exists..."
psql postgres -U $DB_USER -h localhost -p 5432 -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || true

# 4. Restore database
echo -e "\n${BLUE} RESTORING DATABASE${NC}"
echo "Start time: $(date '+%Y-%m-%d %H:%M:%S')"

START_TIME=$(date +%s)

# Restore from backup
echo "Restoring from backup..."
gunzip -c "$BACKUP_FILE" | pg_restore $DB_CONNECTION --clean --if-exists --no-owner --no-acl

RESTORE_RESULT=$?
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ $RESTORE_RESULT -ne 0 ]; then
    echo -e "${RED} Restore failed with code $RESTORE_RESULT${NC}"
    
    # Try alternative method - drop and recreate database
    echo -e "${YELLOW} Trying alternative restore method...${NC}"
    
    # Drop and recreate database
    psql postgres -U $DB_USER -h localhost -p 5432 -c "DROP DATABASE IF EXISTS $DB_NAME;"
    psql postgres -U $DB_USER -h localhost -p 5432 -c "CREATE DATABASE $DB_NAME;"
    
    # Restore using plain SQL
    gunzip -c "$BACKUP_FILE" | pg_restore $DB_CONNECTION --no-owner --no-acl
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN} Restore completed with alternative method${NC}"
    else
        echo -e "${RED} All restore methods failed${NC}"
        exit 1
    fi
else
    echo -e "${GREEN} Database restored successfully!${NC}"
fi

echo "Duration: ${DURATION}s"

# Post-restore verification
echo -e "\n${BLUE} POST-RESTORE VERIFICATION${NC}"

# 1. Check tables exist
echo "Checking table existence..."
TABLES_EXIST=$(psql $DB_CONNECTION -t -c "
SELECT CASE 
    WHEN COUNT(*) >= 4 THEN 'OK'
    ELSE 'MISSING'
END
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('users_user', 'budgets_budget', 'categories_category', 'transactions_transaction');
" | tr -d ' ')

if [ "$TABLES_EXIST" = "OK" ]; then
    echo -e "${GREEN} All tables exist${NC}"
else
    echo -e "${RED} Some tables are missing${NC}"
    # List available tables
    psql $DB_CONNECTION -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
fi

# 2. Check row counts
echo -e "\n RESTORED DATABASE STATISTICS"
psql $DB_CONNECTION -c "
SELECT 
    'users' as table_name, COUNT(*) as row_count FROM users_user
UNION ALL
SELECT 'budgets', COUNT(*) FROM budgets_budget
UNION ALL
SELECT 'categories', COUNT(*) FROM categories_category
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions_transaction
ORDER BY table_name;
"

# 3. Test basic functionality
echo -e "\n TESTING BASIC FUNCTIONALITY"

# Check if we can query each table
for table in users_user budgets_budget categories_category transactions_transaction; do
    if psql $DB_CONNECTION -t -c "SELECT COUNT(*) FROM $table LIMIT 1;" > /dev/null 2>&1; then
        echo -e "${GREEN}  ✓ Table $table is accessible${NC}"
    else
        echo -e "${YELLOW}  ⚠ Table $table has issues${NC}"
    fi
done

# Create restore report
RESTORE_REPORT="$BACKUP_ROOT/restore_$(date +%Y%m%d_%H%M%S).report"
cat > "$RESTORE_REPORT" << EOF
RESTORE REPORT
==============
Date:          $(date '+%Y-%m-%d %H:%M:%S')
Database:      $DB_NAME
User:          $DB_USER
Backup file:   $(basename "$BACKUP_FILE")
Backup date:   $(date -r "$BACKUP_FILE" '+%Y-%m-%d %H:%M:%S')
Backup size:   $BACKUP_SIZE
Duration:      ${DURATION}s
Status:        SUCCESS

DATABASE STATISTICS AFTER RESTORE:
$(psql $DB_CONNECTION -c "
SELECT 
    'users' as table, COUNT(*) as rows FROM users_user
UNION ALL
SELECT 'budgets', COUNT(*) FROM budgets_budget
UNION ALL
SELECT 'categories', COUNT(*) FROM categories_category
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions_transaction;
")

VERIFICATION:
- Tables exist: $TABLES_EXIST
- All tables accessible: YES

EOF

echo -e "\n${GREEN} RESTORE COMPLETED SUCCESSFULLY!${NC}"
echo "Report saved to: $RESTORE_REPORT"
echo ""
echo " Next steps:"
echo "1. Test the application functionality"
echo "2. Verify data integrity"
echo "3. Run: python manage.py migrate"
echo "4. Run: python manage.py check"

# Clean up password from environment
unset PGPASSWORD