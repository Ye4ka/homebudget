#!/bin/bash
# test_backup_restore.sh - Тестирование системы резервного копирования

echo "🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ BACKUP/RESTORE"
echo "========================================"

# 1. Проверка наличия скриптов
echo "1. Проверка скриптов..."
for script in backup.sh restore.sh; do
    if [ -f "scripts/$script" ]; then
        echo "   ✅ $script найден"
        chmod +x "scripts/$script"
    else
        echo "   ❌ $script не найден"
        exit 1
    fi
done

# 2. Создание тестовой резервной копии
echo ""
echo "2. Создание тестовой резервной копии..."
mkdir -p /tmp/test_backups
mkdir -p /tmp/test_logs

# Временное изменение конфигурации
export BACKUP_DIR="/tmp/test_backups"
export LOG_FILE="/tmp/test_logs/backup_test.log"

# Запуск backup.sh (упрощенная версия)
echo "   Запуск процедуры backup..."
if bash scripts/backup.sh > /tmp/test_logs/backup_output.log 2>&1; then
    echo "   ✅ Backup создан успешно"
    
    # Проверка существования файла
    BACKUP_FILE=$(ls -t /tmp/test_backups/homebudget_*.sql.gz 2>/dev/null | head -1)
    if [ -n "$BACKUP_FILE" ]; then
        echo "   📦 Файл резервной копии: $BACKUP_FILE"
        echo "   📏 Размер: $(du -h "$BACKUP_FILE" | cut -f1)"
    else
        echo "   ❌ Файл резервной копии не найден"
        exit 1
    fi
else
    echo "   ❌ Ошибка при создании backup"
    cat /tmp/test_logs/backup_output.log
    exit 1
fi

# 3. Проверка целостности архива
echo ""
echo "3. Проверка целостности архива..."
if gzip -t "$BACKUP_FILE"; then
    echo "   ✅ Архив не поврежден"
else
    echo "   ❌ Архив поврежден"
    exit 1
fi

# 4. Проверка содержимого SQL
echo ""
echo "4. Проверка содержимого SQL..."
SQL_CONTENT=$(zcat "$BACKUP_FILE" | head -20)
if echo "$SQL_CONTENT" | grep -q "PostgreSQL database dump"; then
    echo "   ✅ Формат SQL дампа правильный"
else
    echo "   ⚠️  Возможно неправильный формат дампа"
fi

# 5. Тестирование восстановления (в тестовую БД)
echo ""
echo "5. Тестирование восстановления в тестовую БД..."

# Создаем тестовую БД
TEST_DB="homebudget_test_$(date +%s)"
echo "   Создание тестовой БД: $TEST_DB"

# Проверяем, что можем подключиться к PostgreSQL
if createdb -h localhost -U myuser "$TEST_DB" 2>/dev/null; then
    echo "   ✅ Тестовая БД создана"
    
    # Пробуем восстановить
    echo "   Восстановление из backup..."
    if zcat "$BACKUP_FILE" | psql -h localhost -U myuser -d "$TEST_DB" --quiet 2>/dev/null; then
        echo "   ✅ Восстановление прошло успешно"
        
        # Проверяем таблицы в восстановленной БД
        TABLES_COUNT=$(psql -h localhost -U myuser -d "$TEST_DB" -t \
            -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
        echo "   📊 Таблиц в восстановленной БД: $TABLES_COUNT"
        
        # Удаляем тестовую БД
        dropdb -h localhost -U myuser "$TEST_DB"
        echo "   🧹 Тестовая БД удалена"
    else
        echo "   ❌ Ошибка восстановления"
        dropdb -h localhost -U myuser "$TEST_DB"
        exit 1
    fi
else
    echo "   ❌ Не удалось создать тестовую БД"
    exit 1
fi

# 6. Очистка тестовых данных
echo ""
echo "6. Очистка тестовых данных..."
rm -rf /tmp/test_backups /tmp/test_logs
echo "   ✅ Тестовые данные очищены"

echo ""
echo "========================================"
echo "🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!"
echo "Система backup/restore работает корректно."