-- 1. Баланс бюджета за период с детализацией
SELECT 
    b.id as budget_id,
    b.name as budget_name,
    b.type as budget_type,
    b.currency,
    u.username as owner,
    
    -- Статистика за период
    COUNT(t.id) as transactions_in_period,
    SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END) as period_income,
    SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END) as period_expense,
    SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE -t.amount END) as period_balance,
    
    -- Средние показатели
    ROUND(AVG(CASE WHEN t.type = 'income' THEN t.amount END), 2) as avg_income,
    ROUND(AVG(CASE WHEN t.type = 'expense' THEN t.amount END), 2) as avg_expense,
    
    -- Первая и последняя транзакция в периоде
    MIN(t.date) as first_transaction_date,
    MAX(t.date) as last_transaction_date
    
FROM budgets_budget b
JOIN users_user u ON b.owner_id = u.id
LEFT JOIN transactions_transaction t ON b.id = t.budget_id
    AND t.date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY b.id, b.name, b.type, b.currency, u.username
ORDER BY period_balance DESC;