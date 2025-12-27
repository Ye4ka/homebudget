
# Настройка текущей базы данных

echo "НАСТРОЙКА ТЕКУЩЕЙ БАЗЫ ДАННЫХ"
echo "=================================="

# Проверка подключения
if [ -z "$DATABASE_URL" ]; then
    echo "Ошибка: DATABASE_URL не установлен"
    echo "Добавьте в .env: DATABASE_URL=postgresql://myuser:@localhost:5432/homebudget"
    exit 1
fi

# 1. Создание индексов
echo "1. Создание индексов..."
python scripts/create_indexes_current.py

# 2. Создание представлений
echo "2. Создание аналитических представлений..."
psql "$DATABASE_URL" -f sql/views/create_views_current.sql

# 3. Тестирование запросов
echo "3. Тестирование аналитических запросов..."
echo "   Баланс бюджетов:"
psql "$DATABASE_URL" -c "SELECT budget_name, currency, balance FROM budget_summary ORDER BY balance DESC LIMIT 5;"

echo "   Топ категорий:"
psql "$DATABASE_URL" -c "SELECT category_name, total_amount FROM category_summary WHERE category_type = 'expense' ORDER BY total_amount DESC LIMIT 5;"

echo "   Месячная статистика:"
psql "$DATABASE_URL" -c "SELECT month_start, transaction_count, total_income, total_expense FROM monthly_summary ORDER BY month_start DESC LIMIT 3;"

# 4. Создание документации
echo "4. Создание документации..."
mkdir -p docs/database

# Создать README с информацией о структуре
cat > docs/database/current_structure.md << 'EOF'
# Текущая структура базы данных

## Таблицы

### users_user
- id (PK)
- username
- email  
- first_name
- last_name
- currency
- password
- is_superuser, is_staff, is_active
- date_joined, last_login

### budgets_budget
- id (PK)
- name
- type (personal/family)
- currency (RUB/USD/EUR/KZT)
- owner_id (FK → users_user)
- created_at, updated_at

### categories_category
- id (PK)
- name
- type (income/expense)
- color (HEX)
- icon
- budget_id (FK → budgets_budget, может быть NULL)
- created_by_id (FK → users_user)
- created_at

### transactions_transaction
- id (PK)
- amount
- type (income/expense)
- description
- date
- category_id (FK → categories_category)
- budget_id (FK → budgets_budget)
- created_by_id (FK → users_user)
- created_at

### budgets_budgetmember
- id (PK)
- budget_id (FK → budgets_budget)
- user_id (FK → users_user)
- role (owner/editor/viewer)
- joined_at

## Индексы
(см. scripts/create_indexes_current.py)

## Представления
1. budget_summary - сводка по бюджетам
2. category_summary - сводка по категориям
3. monthly_summary - месячная статистика (материализованное)
EOF

echo ""
echo "✅ НАСТРОЙКА ЗАВЕРШЕНА!"
echo "База данных оптимизирована для аналитических запросов"