#!/bin/bash
# Настройка базы данных с явными учетными данными

echo " НАСТРОЙКА БАЗЫ ДАННЫХ HomeBudget"
echo "=================================="

# Параметры подключения
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="homebudget"
DB_USER="myuser"
DB_PASS="mypassword"

# 1. Проверка подключения
echo "1. Проверка подключения к базе..."
PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT version();" 2>/dev/null

if [ $? -ne 0 ]; then
    echo " Не удалось подключиться к базе данных"
    echo "   Проверьте:"
    echo "   - Запущен ли PostgreSQL"
    echo "   - Правильность учетных данных"
    echo "   - Существует ли база '$DB_NAME'"
    exit 1
fi

echo " Подключение успешно"

# 2. Создание индексов
echo "2. Создание индексов..."
python scripts/create_indexes_current.py

# 3. Создание представлений
echo "3. Создание аналитических представлений..."
PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME \
    -f sql/views/create_views_current.sql 2>&1 | grep -v "NOTICE"

# 4. Тестирование
echo "4. Тестирование представлений..."
echo "   Бюджеты:"
PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME \
    -c "SELECT budget_name, currency, balance FROM budget_summary ORDER BY balance DESC LIMIT 3;" 2>/dev/null

echo "   Категории:"
PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME \
    -c "SELECT category_name, total_amount FROM category_summary WHERE category_type = 'expense' ORDER BY total_amount DESC LIMIT 3;" 2>/dev/null

echo ""
echo " НАСТРОЙКА ЗАВЕРШЕНА!"