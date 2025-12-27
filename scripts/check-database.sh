echo "Введите пароль PostgreSQL для пользователя postgres:"
read -s PASSWORD
export PGPASSWORD="$PASSWORD"
DB_NAME="homebudget"
DB_USER="myuser" 
OUTPUT_FILE="logs/db-monitor-$(date +%Y%m%d_%H%M%S).log"

mkdir -p logs

echo "=== DATABASE MONITORING REPORT ===" > "$OUTPUT_FILE"
echo "Generated: $(date)" >> "$OUTPUT_FILE"
echo "Database: $DB_NAME" >> "$OUTPUT_FILE"
echo "User: $DB_USER" >> "$OUTPUT_FILE"
echo "==================================" >> "$OUTPUT_FILE"

# Запрос пароля один раз
echo -n "Введите пароль для пользователя $DB_USER: "
read -s PASSWORD
echo
export PGPASSWORD="$PASSWORD"

# 1. Общая статистика
echo "" >> "$OUTPUT_FILE"
echo "1. ОБЩАЯ СТАТИСТИКА:" >> "$OUTPUT_FILE"
psql -h localhost -U "$DB_USER" -d "$DB_NAME" -c "
SELECT 
    (SELECT COUNT(*) FROM users_user) as total_users,
    (SELECT COUNT(*) FROM budgets_budget) as total_budgets,
    (SELECT COUNT(*) FROM categories_category) as total_categories,
    (SELECT COUNT(*) FROM transactions_transaction) as total_transactions,
    (SELECT COALESCE(SUM(amount), 0) FROM transactions_transaction WHERE type = 'income') as total_income,
    (SELECT COALESCE(SUM(amount), 0) FROM transactions_transaction WHERE type = 'expense') as total_expense,
    (SELECT COALESCE(SUM(amount), 0) FROM transactions_transaction WHERE type = 'income') - 
    (SELECT COALESCE(SUM(amount), 0) FROM transactions_transaction WHERE type = 'expense') as net_balance;
" >> "$OUTPUT_FILE" 2>/dev/null || echo "Ошибка подключения к БД" >> "$OUTPUT_FILE"

# 2. Топ категорий расходов
echo "" >> "$OUTPUT_FILE"
echo "2. ТОП-5 КАТЕГОРИЙ ПО РАСХОДАМ (30 дней):" >> "$OUTPUT_FILE"
psql -h localhost -U "$DB_USER" -d "$DB_NAME" -c "
SELECT 
    c.name as category,
    COUNT(t.id) as transactions,
    SUM(t.amount) as total_spent,
    ROUND(AVG(t.amount), 2) as avg_amount
FROM transactions_transaction t
JOIN categories_category c ON t.category_id = c.id
WHERE t.type = 'expense' 
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.id, c.name
ORDER BY total_spent DESC
LIMIT 5;
" >> "$OUTPUT_FILE" 2>/dev/null || echo "Ошибка выполнения запроса" >> "$OUTPUT_FILE"

# 3. Средний чек
echo "" >> "$OUTPUT_FILE"
echo "3. СРЕДНИЙ ЧЕК ТРАНЗАКЦИЙ:" >> "$OUTPUT_FILE"
psql -h localhost -U "$DB_USER" -d "$DB_NAME" -c "
SELECT 
    type,
    COUNT(*) as count,
    ROUND(AVG(amount), 2) as avg_check,
    MIN(amount) as min,
    MAX(amount) as max
FROM transactions_transaction 
GROUP BY type;
" >> "$OUTPUT_FILE" 2>/dev/null || echo "Ошибка выполнения запроса" >> "$OUTPUT_FILE"

# Очистка пароля из памяти
unset PGPASSWORD

echo "" >> "$OUTPUT_FILE"
echo "=== REPORT SAVED TO: $OUTPUT_FILE ==="
echo "View with: cat $OUTPUT_FILE"
echo ""
echo "Содержимое отчета:"
echo "------------------"
cat "$OUTPUT_FILE"
EOF

chmod +x scripts/check-database.sh