# КОНФИГУРАЦИЯ
DB_NAME="homebudget"
DB_USER="myuser"
BACKUP_DIR="./backups"
LOG_FILE="./logs/backup.log"
TEMP_DIR="/tmp/homebudget_restore_$(date +%s)"


# ФУНКЦИИ

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_prerequisites() {
    log_message "Проверка предварительных условий..."

    if [ ! -d "$BACKUP_DIR" ]; then
        log_message "ОШИБКА: Директория с резервными копиями не найдена: $BACKUP_DIR"
        exit 1
    fi

    local backup_files=("$BACKUP_DIR"/${DB_NAME}_*.sql.gz)
    if [ ${#backup_files[@]} -eq 0 ]; then
        log_message "ОШИБКА: Резервные копии не найдены"
        exit 1
    fi
 
    if ! pg_isready -h localhost -U "$DB_USER" > /dev/null 2>&1; then
        log_message "ОШИБКА: PostgreSQL не доступен"
        exit 1
    fi

    mkdir -p "$TEMP_DIR"
    
    log_message "Предварительные проверки пройдены"
}

list_backups() {
    log_message "Доступные резервные копии:"
    local counter=1
    for file in "$BACKUP_DIR"/${DB_NAME}_*.sql.gz; do
        local size=$(du -h "$file" | cut -f1)
        local date=$(stat -c %y "$file" | cut -d' ' -f1)
        echo "  $counter. $file ($size, $date)"
        ((counter++))
    done
}

validate_backup() {
    local backup_file=$1
    
    log_message "Проверка целостности резервной копии..."

    if [ ! -f "$backup_file" ]; then
        log_message "ОШИБКА: Файл не найден: $backup_file"
        return 1
    fi
    
   
    if ! gzip -t "$backup_file"; then
        log_message "ОШИБКА: Архив поврежден: $backup_file"
        return 1
    fi
    
    
    local sql_header=$(zcat "$backup_file" | head -5)
    if ! echo "$sql_header" | grep -q "PostgreSQL database dump"; then
        log_message "ВНИМАНИЕ: Файл может быть не SQL дампом PostgreSQL"
    fi
    
    log_message "Резервная копия валидна: $backup_file"
    return 0
}

backup_current_db() {
    log_message "Создание резервной копии текущей базы данных перед восстановлением..."
    
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local pre_restore_backup="${BACKUP_DIR}/pre_restore_${DB_NAME}_${timestamp}.sql.gz"
    
    if pg_dump -h localhost -U "$DB_USER" -d "$DB_NAME" | gzip > "$pre_restore_backup"; then
        local size=$(du -h "$pre_restore_backup" | cut -f1)
        log_message "Резервная копия создана: $pre_restore_backup ($size)"
    else
        log_message "ВНИМАНИЕ: Не удалось создать резервную копию текущей БД"
    fi
}

terminate_connections() {
    log_message "🔌 Завершение активных подключений к базе данных..."
    
    psql -h localhost -U "$DB_USER" -d postgres << EOF
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = '$DB_NAME'
  AND pid <> pg_backend_pid();
EOF
    
    
    sleep 2
    
    log_message "Активные подключения завершены"
}

drop_and_recreate_db() {
    log_message "Подготовка базы данных к восстановлению..."
    
    
    if psql -h localhost -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        log_message "Текущая БД существует, удаляем..."
        
 
        dropdb -h localhost -U "$DB_USER" "$DB_NAME" --if-exists
        
        if [ $? -eq 0 ]; then
            log_message "База данных удалена"
        else
            log_message "ОШИБКА: Не удалось удалить базу данных"
            return 1
        fi
    fi
    

    log_message "Создание новой базы данных..."
    
    createdb -h localhost -U "$DB_USER" "$DB_NAME" \
        --encoding=UTF8 \
        --locale=en_US.UTF-8 \
        --template=template0
    
    if [ $? -eq 0 ]; then
        log_message "База данных создана: $DB_NAME"
        return 0
    else
        log_message "ОШИБКА: Не удалось создать базу данных"
        return 1
    fi
}

restore_database() {
    local backup_file=$1
    
    log_message "🔄 Восстановление базы данных из: $backup_file"
    
 
    if zcat "$backup_file" | psql -h localhost -U "$DB_USER" -d "$DB_NAME" --quiet; then
        log_message "База данных восстановлена"
        return 0
    else
        log_message "ОШИБКА: Восстановление не удалось"
        return 1
    fi
}

verify_restoration() {
    log_message "Проверка восстановленной базы данных..."

    local table_count=$(psql -h localhost -U "$DB_USER" -d "$DB_NAME" -t \
        -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
    
 
    local users_count=$(psql -h localhost -U "$DB_USER" -d "$DB_NAME" -t \
        -c "SELECT COUNT(*) FROM users_user;" | tr -d ' ')
    
    local transactions_count=$(psql -h localhost -U "$DB_USER" -d "$DB_NAME" -t \
        -c "SELECT COUNT(*) FROM transactions_transaction;" | tr -d ' ')
    
    log_message "Статистика восстановленной БД:"
    log_message "   - Таблиц: $table_count"
    log_message "   - Пользователей: $users_count"
    log_message "   - Транзакций: $transactions_count"
    
   
    if psql -h localhost -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
        log_message "Проверка целостности пройдена"
        return 0
    else
        log_message "ОШИБКА: Проблема с целостностью данных"
        return 1
    fi
}

cleanup_temp() {
    log_message "Очистка временных файлов..."
    rm -rf "$TEMP_DIR"
    log_message " Временные файлы удалены"
}


# ОСНОВНАЯ ПРОГРАММА

main() {
    log_message "========================================="
    log_message "ЗАПУСК ПРОЦЕДУРЫ ВОССТАНОВЛЕНИЯ БАЗЫ ДАННЫХ"
 
    check_prerequisites
    
   
    list_backups
    
 
    if [ -n "$1" ]; then
        BACKUP_FILE="$1"
    else
    
        BACKUP_FILE=$(ls -t "$BACKUP_DIR"/${DB_NAME}_*.sql.gz | head -1)
    fi
    
    log_message "Выбрана резервная копия: $BACKUP_FILE"
    

    if ! validate_backup "$BACKUP_FILE"; then
        exit 1
    fi
   
    backup_current_db
  
    terminate_connections

    if ! drop_and_recreate_db; then
        exit 1
    fi

    if ! restore_database "$BACKUP_FILE"; then
        exit 1
    fi

    if ! verify_restoration; then
        exit 1
    fi

    cleanup_temp
    
    log_message "ВОССТАНОВЛЕНИЕ УСПЕШНО ЗАВЕРШЕНО"
    log_message "========================================="

    echo ""
    echo "Восстановление завершено успешно!"
    echo "Для проверки можно выполнить:"
    echo "   psql -U $DB_USER -d $DB_NAME -c 'SELECT COUNT(*) FROM users_user;'"
    echo "   psql -U $DB_USER -d $DB_NAME -c 'SELECT COUNT(*) FROM transactions_transaction;'"
}

main "$@"