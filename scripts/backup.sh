# КОНФИГУРАЦИЯ
DB_NAME="homebudget"
DB_USER="myuser"
BACKUP_DIR="./backups"
LOG_FILE="./logs/backup.log"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

# ФУНКЦИИ

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_prerequisites() {
    mkdir -p "$BACKUP_DIR"
    mkdir -p "/var/log/homebudget"
      
    if [ ! -w "$BACKUP_DIR" ]; then
        log_message "ОШИБКА: Нет прав на запись в $BACKUP_DIR"
        exit 1
    fi

    if ! pg_isready -h localhost -U "$DB_USER" > /dev/null 2>&1; then
        log_message "ОШИБКА: PostgreSQL не доступен"
        exit 1
    fi
}

perform_backup() {
    log_message "Запуск резервного копирования БД: $DB_NAME"

    log_message "Создание дампа базы данных..."
    if pg_dump -h localhost -U "$DB_USER" -d "$DB_NAME" \
        --no-password \
        --verbose \
        --format=plain \
        --encoding=UTF8 \
        --no-owner \
        --no-privileges | gzip > "$BACKUP_FILE"; then

        BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        log_message "Резервная копия создана: $BACKUP_FILE ($BACKUP_SIZE)"

        if gzip -t "$BACKUP_FILE"; then
            log_message "Целостность архива проверена"
        else
            log_message "ВНИМАНИЕ: Проблема с целостностью архива"
        fi
    else
        log_message "ОШИБКА: Не удалось создать резервную копию"
        exit 1
    fi
}

rotate_backups() {
    log_message "Ротация резервных копий (сохранение за $RETENTION_DAYS дней)..."

    find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

    BACKUP_COUNT=$(find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -type f | wc -l)
    log_message "Осталось резервных копий: $BACKUP_COUNT"

    log_message "Текущие резервные копии:"
    find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -type f -exec ls -lh {} \; | tee -a "$LOG_FILE"
}

cleanup() {
    log_message "Очистка временных файлов..."
    find /tmp -name "pg_dump_*" -type f -mtime +3 -delete 2>/dev/null || true
}

send_notification() {
    local status=$1
    local message=$2
    
    log_message "Уведомление отправлено: $status - $message"
}
# ОСНОВНАЯ ПРОГРАММА
main() {
    log_message "========================================="
    log_message "ЗАПУСК ПРОЦЕДУРЫ РЕЗЕРВНОГО КОПИРОВАНИЯ"
    

    check_prerequisites
    
    if perform_backup; then
        rotate_backups       
        cleanup
        
   
        send_notification "SUCCESS" "Backup completed successfully. Size: $BACKUP_SIZE"
        
        log_message "РЕЗЕРВНОЕ КОПИРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО"
    else
        send_notification "FAILED" "Backup failed. Check logs: $LOG_FILE"
        
        log_message "РЕЗЕРВНОЕ КОПИРОВАНИЕ ЗАВЕРШИЛОСЬ С ОШИБКОЙ"
        exit 1
    fi
    
    log_message "========================================="
}

main