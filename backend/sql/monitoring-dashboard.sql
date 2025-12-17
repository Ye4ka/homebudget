-- ============================================
-- МОНИТОРИНГ БАЗЫ ДАННЫХ HOMEBUDGET
-- monitoring-dashboard.sql
-- ============================================

-- 1. ОБЩАЯ СТАТИСТИКА ПО ТАБЛИЦАМ
SELECT 
    schemaname as schema,
    tablename as table_name,
    tableowner as owner,
    tablespace,
    hasindexes as has_indexes,
    hasrules as has_rules,
    hastriggers as has_triggers,
    rowsecurity as row_security
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- 2. КОЛИЧЕСТВО ЗАПИСЕЙ В КАЖДОЙ ТАБЛИЦЕ
SELECT 
    schemaname as schema,
    relname as table_name,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables 
ORDER BY n_live_tup DESC;

-- 3. САМЫЕ КРУПНЫЕ ТАБЛИЦЫ (ПО РАЗМЕРУ)
SELECT 
    schemaname as schema,
    tablename as table_name,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename) - 
                   pg_relation_size(schemaname || '.' || tablename)) as index_size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;

-- 4. ТОП-5 КАТЕГОРИЙ ПО РАСХОДАМ (ЗА ПОСЛЕДНИЕ 30 ДНЕЙ)
SELECT 
    c.name as category_name,
    c.type,
    c.color,
    COUNT(t.id) as transaction_count,
    SUM(t.amount) as total_amount,
    ROUND(AVG(t.amount), 2) as average_amount,
    MIN(t.amount) as min_amount,
    MAX(t.amount) as max_amount
FROM transactions_transaction t
JOIN categories_category c ON t.category_id = c.id
WHERE t.type = 'expense'
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.id, c.name, c.type, c.color
ORDER BY total_amount DESC
LIMIT 5;

-- 5. СРЕДНИЙ ЧЕК ТРАНЗАКЦИЙ
SELECT 
    type,
    COUNT(*) as transaction_count,
    ROUND(AVG(amount), 2) as avg_check,
    MIN(amount) as min_check,
    MAX(amount) as max_check,
    ROUND(STDDEV(amount), 2) as std_dev,
    SUM(amount) as total_amount
FROM transactions_transaction 
GROUP BY type
ORDER BY type;

-- 6. АКТИВНОСТЬ ПОЛЬЗОВАТЕЛЕЙ
SELECT 
    u.username,
    u.email,
    COUNT(t.id) as total_transactions,
    COUNT(CASE WHEN t.type = 'income' THEN 1 END) as income_count,
    COUNT(CASE WHEN t.type = 'expense' THEN 1 END) as expense_count,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount END), 0) as total_income,
    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount END), 0) as total_expense,
    MAX(t.date) as last_transaction_date
FROM users_user u
LEFT JOIN transactions_transaction t ON u.id = t.created_by
GROUP BY u.id, u.username, u.email
ORDER BY total_transactions DESC;

-- 7. СТАТИСТИКА ПО БЮДЖЕТАМ
SELECT 
    b.name as budget_name,
    b.type as budget_type,
    b.currency,
    COUNT(t.id) as transaction_count,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount END), 0) as total_income,
    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount END), 0) as total_expense,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount END), 0) - 
    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount END), 0) as current_balance,
    MIN(t.date) as first_transaction,
    MAX(t.date) as last_transaction
FROM budgets_budget b
LEFT JOIN transactions_transaction t ON b.id = t.budget_id
GROUP BY b.id, b.name, b.type, b.currency
ORDER BY current_balance DESC;

-- 8. ЕЖЕДНЕВНАЯ АКТИВНОСТЬ (ПОСЛЕДНИЕ 7 ДНЕЙ)
SELECT 
    date,
    COUNT(*) as transactions_per_day,
    COUNT(CASE WHEN type = 'income' THEN 1 END) as income_count,
    COUNT(CASE WHEN type = 'expense' THEN 1 END) as expense_count,
    COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) as daily_income,
    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) as daily_expense
FROM transactions_transaction 
WHERE date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY date
ORDER BY date DESC;

-- 9. МОНИТОРИНГ ИНДЕКСОВ
SELECT 
    schemaname as schema,
    tablename as table_name,
    indexname as index_name,
    indexdef as index_definition,
    pg_size_pretty(pg_relation_size(schemaname || '.' || indexname)) as index_size
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- 10. СТАТИСТИКА ПО САМЫМ АКТИВНЫМ ДНЯМ НЕДЕЛИ
SELECT 
    EXTRACT(DOW FROM date) as day_of_week,
    CASE EXTRACT(DOW FROM date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_name,
    COUNT(*) as transaction_count,
    ROUND(AVG(amount), 2) as avg_amount,
    SUM(amount) as total_amount
FROM transactions_transaction 
GROUP BY EXTRACT(DOW FROM date), day_name
ORDER BY transaction_count DESC;

-- 11. ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ
SELECT 
    'Users without budgets' as check_type,
    COUNT(*) as count
FROM users_user u
LEFT JOIN budgets_budget b ON u.id = b.owner_id
WHERE b.id IS NULL
UNION ALL
SELECT 
    'Transactions without category' as check_type,
    COUNT(*) as count
FROM transactions_transaction t
LEFT JOIN categories_category c ON t.category_id = c.id
WHERE c.id IS NULL
UNION ALL
SELECT 
    'Categories without transactions (last 30 days)' as check_type,
    COUNT(*) as count
FROM categories_category c
LEFT JOIN transactions_transaction t ON c.id = t.category_id 
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
WHERE t.id IS NULL;

-- 12. СВОДНЫЙ ОТЧЕТ (SUMMARY)
SELECT 
    (SELECT COUNT(*) FROM users_user) as total_users,
    (SELECT COUNT(*) FROM budgets_budget) as total_budgets,
    (SELECT COUNT(*) FROM categories_category) as total_categories,
    (SELECT COUNT(*) FROM transactions_transaction) as total_transactions,
    (SELECT COUNT(*) FROM transactions_transaction WHERE type = 'income') as income_transactions,
    (SELECT COUNT(*) FROM transactions_transaction WHERE type = 'expense') as expense_transactions,
    (SELECT COALESCE(SUM(amount), 0) FROM transactions_transaction WHERE type = 'income') as total_income,
    (SELECT COALESCE(SUM(amount), 0) FROM transactions_transaction WHERE type = 'expense') as total_expense,
    (SELECT COALESCE(SUM(amount), 0) FROM transactions_transaction WHERE type = 'income') - 
    (SELECT COALESCE(SUM(amount), 0) FROM transactions_transaction WHERE type = 'expense') as net_balance;

-- ============================================
-- ДЛЯ БЫСТРОГО МОНИТОРИНГА (ОДНОСТРОЧНЫЕ ЗАПРОСЫ)
-- ============================================

-- Текущий размер БД
SELECT pg_size_pretty(pg_database_size('homebudget')) as db_size;

-- Количество подключений
SELECT COUNT(*) as active_connections FROM pg_stat_activity 
WHERE datname = 'homebudget';

-- Дата последнего VACUUM
SELECT schemaname, relname, last_vacuum, last_autovacuum 
FROM pg_stat_user_tables 
ORDER BY last_vacuum DESC NULLS LAST 
LIMIT 5;

-- Самые частые запросы (если включен pg_stat_statements)
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;