-- Создание представлений для текущей структуры

-- 1. Представление сводки по бюджетам
CREATE OR REPLACE VIEW budget_summary AS
SELECT 
    b.id,
    b.name as budget_name,
    b.type as budget_type,
    b.currency,
    u.username as owner_username,
    u.email as owner_email,
    COUNT(t.id) as transaction_count,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expense,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE -t.amount END), 0) as balance,
    MIN(t.date) as first_transaction,
    MAX(t.date) as last_transaction
FROM budgets_budget b
JOIN users_user u ON b.owner_id = u.id
LEFT JOIN transactions_transaction t ON b.id = t.budget_id
GROUP BY b.id, b.name, b.type, b.currency, u.username, u.email;

-- 2. Представление сводки по категориям
CREATE OR REPLACE VIEW category_summary AS
SELECT 
    c.id,
    c.name as category_name,
    c.type as category_type,
    c.color,
    c.icon,
    COUNT(t.id) as transaction_count,
    COALESCE(SUM(t.amount), 0) as total_amount,
    COALESCE(AVG(t.amount), 0) as average_amount,
    MIN(t.date) as first_transaction,
    MAX(t.date) as last_transaction,
    COUNT(DISTINCT t.budget_id) as budget_count
FROM categories_category c
LEFT JOIN transactions_transaction t ON c.id = t.category_id
GROUP BY c.id, c.name, c.type, c.color, c.icon;

-- 3. Материализованное представление для месячной статистики
DROP MATERIALIZED VIEW IF EXISTS monthly_summary;

CREATE MATERIALIZED VIEW monthly_summary AS
SELECT 
    DATE_TRUNC('month', t.date)::DATE as month_start,
    EXTRACT(YEAR FROM t.date) as year,
    EXTRACT(MONTH FROM t.date) as month,
    COUNT(t.id) as transaction_count,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expense,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE -t.amount END), 0) as balance,
    COUNT(DISTINCT t.budget_id) as budget_count,
    COUNT(DISTINCT t.category_id) as category_count
FROM transactions_transaction t
WHERE t.date IS NOT NULL
GROUP BY DATE_TRUNC('month', t.date), EXTRACT(YEAR FROM t.date), EXTRACT(MONTH FROM t.date)
ORDER BY year DESC, month DESC;

-- Создать индекс для быстрого обновления (отдельной командой)
CREATE UNIQUE INDEX IF NOT EXISTS idx_monthly_summary_date ON monthly_summary (month_start);

-- Функция для обновления материализованного представления
CREATE OR REPLACE FUNCTION refresh_monthly_summary()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_summary;
END;
$$ LANGUAGE plpgsql;

SELECT '✅ Представления успешно созданы' as result;