-- 1. БАЛАНС БЮДЖЕТА ЗА ПЕРИОД
WITH period_transactions AS (
    SELECT 
        budget_id,
        type,
        SUM(amount) as total_amount
    FROM transactions_transaction 
    WHERE budget_id = 1  -- Укажите ID бюджета
        AND date BETWEEN '2024-01-01' AND '2024-12-31'  -- Укажите период
    GROUP BY budget_id, type
)
SELECT 
    b.name as budget_name,
    COALESCE(SUM(CASE WHEN pt.type = 'income' THEN pt.total_amount END), 0) as total_income,
    COALESCE(SUM(CASE WHEN pt.type = 'expense' THEN pt.total_amount END), 0) as total_expense,
    COALESCE(SUM(CASE WHEN pt.type = 'income' THEN pt.total_amount END), 0) - 
    COALESCE(SUM(CASE WHEN pt.type = 'expense' THEN pt.total_amount END), 0) as balance
FROM budgets_budget b
LEFT JOIN period_transactions pt ON b.id = pt.budget_id
WHERE b.id = 1
GROUP BY b.id, b.name;

-- 2. ТОП-5 КАТЕГОРИЙ ПО РАСХОДАМ (ЗА ПОСЛЕДНИЕ 30 ДНЕЙ)
SELECT 
    c.name as category_name,
    c.color,
    c.icon,
    SUM(t.amount) as total_spent,
    COUNT(t.id) as transaction_count,
    ROUND(AVG(t.amount), 2) as average_transaction
FROM transactions_transaction t
JOIN categories_category c ON t.category_id = c.id
WHERE t.type = 'expense'
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
    AND t.budget_id = 1  -- Укажите ID бюджета
GROUP BY c.id, c.name, c.color, c.icon
ORDER BY total_spent DESC
LIMIT 5;

-- 3. ДИНАМИКА БАЛАНСА ПО ДНЯМ (ЗА ПОСЛЕДНИЕ 7 ДНЕЙ)
SELECT 
    date,
    COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) as daily_income,
    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) as daily_expense,
    COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) - 
    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) as daily_balance,
    SUM(COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) - 
        COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0)) 
        OVER (ORDER BY date) as cumulative_balance
FROM transactions_transaction 
WHERE budget_id = 1  -- Укажите ID бюджета
    AND date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY date
ORDER BY date;

-- 4. СРАВНЕНИЕ ДОХОДОВ/РАСХОДОВ ПО МЕСЯЦАМ (ТЕКУЩИЙ ГОД)
SELECT 
    EXTRACT(YEAR FROM date) as year,
    EXTRACT(MONTH FROM date) as month,
    TO_CHAR(date, 'Month') as month_name,
    COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) as monthly_income,
    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) as monthly_expense,
    COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) - 
    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) as monthly_balance
FROM transactions_transaction 
WHERE budget_id = 1  -- Укажите ID бюджета
    AND EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date), TO_CHAR(date, 'Month')
ORDER BY year, month;

-- 5. САМЫЕ КРУПНЫЕ ТРАНЗАКЦИИ
SELECT 
    t.date,
    t.amount,
    t.type,
    t.description,
    c.name as category_name,
    c.color
FROM transactions_transaction t
JOIN categories_category c ON t.category_id = c.id
WHERE t.budget_id = 1
ORDER BY t.amount DESC
LIMIT 10;

-- 6. СРЕДНЕДНЕВНЫЕ РАСХОДЫ ПО КАТЕГОРИЯМ
SELECT 
    c.name as category_name,
    c.color,
    ROUND(SUM(t.amount) / COUNT(DISTINCT t.date), 2) as avg_daily_spent,
    COUNT(t.id) as transaction_count
FROM transactions_transaction t
JOIN categories_category c ON t.category_id = c.id
WHERE t.type = 'expense'
    AND t.budget_id = 1
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.id, c.name, c.color
ORDER BY avg_daily_spent DESC;

-- 7. ПРОГНОЗ РАСХОДОВ НА СЛЕДУЮЩИЙ МЕСЯЦ
WITH monthly_avg AS (
    SELECT 
        EXTRACT(MONTH FROM date) as month,
        c.name as category_name,
        AVG(amount) as avg_monthly_spent
    FROM transactions_transaction t
    JOIN categories_category c ON t.category_id = c.id
    WHERE t.type = 'expense'
        AND t.budget_id = 1
        AND date >= CURRENT_DATE - INTERVAL '6 months'
    GROUP BY EXTRACT(MONTH FROM date), c.id, c.name
)
SELECT 
    category_name,
    ROUND(AVG(avg_monthly_spent), 2) as forecast_next_month
FROM monthly_avg
GROUP BY category_name
ORDER BY forecast_next_month DESC;

-- 8. АКТИВНОСТЬ ПОЛЬЗОВАТЕЛЕЙ (КТО СКОЛЬКО ТРАНЗАКЦИЙ СОЗДАЛ)
SELECT 
    u.username,
    COUNT(t.id) as transactions_created,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount END), 0) as total_income_created,
    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount END), 0) as total_expense_created
FROM users_user u
LEFT JOIN transactions_transaction t ON u.id = t.created_by
WHERE t.budget_id = 1 OR t.id IS NULL
GROUP BY u.id, u.username
ORDER BY transactions_created DESC;

-- 1. VIEW: ЕЖЕМЕСЯЧНАЯ СВОДКА (monthly_summary)
CREATE OR REPLACE VIEW monthly_summary AS
SELECT 
    b.id as budget_id,
    b.name as budget_name,
    EXTRACT(YEAR FROM t.date) as year,
    EXTRACT(MONTH FROM t.date) as month,
    TO_CHAR(t.date, 'Month') as month_name,
    COUNT(t.id) as total_transactions,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount END), 0) as total_income,
    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount END), 0) as total_expense,
    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount END), 0) - 
    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount END), 0) as balance,
    COUNT(DISTINCT t.category_id) as unique_categories
FROM budgets_budget b
LEFT JOIN transactions_transaction t ON b.id = t.budget_id
WHERE t.date IS NOT NULL
GROUP BY b.id, b.name, EXTRACT(YEAR FROM t.date), EXTRACT(MONTH FROM t.date), TO_CHAR(t.date, 'Month')
ORDER BY b.id, year, month;

-- 2. VIEW: СУММЫ ПО КАТЕГОРИЯМ (category_totals)
CREATE OR REPLACE VIEW category_totals AS
SELECT 
    b.id as budget_id,
    b.name as budget_name,
    c.id as category_id,
    c.name as category_name,
    c.type as category_type,
    c.color,
    c.icon,
    COUNT(t.id) as transaction_count,
    COALESCE(SUM(t.amount), 0) as total_amount,
    ROUND(AVG(t.amount), 2) as average_amount,
    MIN(t.date) as first_transaction,
    MAX(t.date) as last_transaction
FROM budgets_budget b
CROSS JOIN categories_category c
LEFT JOIN transactions_transaction t ON b.id = t.budget_id AND c.id = t.category_id
WHERE c.is_default = TRUE OR c.budget_id = b.id
GROUP BY b.id, b.name, c.id, c.name, c.type, c.color, c.icon
ORDER BY b.id, c.type, total_amount DESC;

-- Тест 1: Проверка monthly_summary
SELECT * FROM monthly_summary WHERE budget_id = 1 ORDER BY year, month;

-- Тест 2: Проверка category_totals
SELECT * FROM category_totals WHERE budget_id = 1 AND category_type = 'expense' ORDER BY total_amount DESC;

-- Тест 3: Общая статистика по бюджету
SELECT 
    budget_name,
    SUM(total_income) as year_income,
    SUM(total_expense) as year_expense,
    SUM(balance) as year_balance
FROM monthly_summary 
WHERE budget_id = 1 
GROUP BY budget_id, budget_name;