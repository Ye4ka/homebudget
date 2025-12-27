-- 2. Топ-5 категорий по расходам с анализом
SELECT 
    c.id as category_id,
    c.name as category_name,
    c.type as category_type,
    c.color,
    
    -- Основная статистика
    COUNT(t.id) as transaction_count,
    SUM(t.amount) as total_amount,
    ROUND(AVG(t.amount), 2) as average_amount,
    MIN(t.amount) as min_amount,
    MAX(t.amount) as max_amount,
    
    -- Распределение по бюджетам
    COUNT(DISTINCT t.budget_id) as budget_count,
    
    -- Динамика
    MIN(t.date) as first_usage,
    MAX(t.date) as last_usage,
    
    -- Доля от общих расходов
    ROUND(
        SUM(t.amount) * 100.0 / NULLIF(
            (SELECT SUM(amount) FROM transactions_transaction WHERE type = 'expense' AND date BETWEEN '2024-01-01' AND '2024-01-31'), 
            0
        ), 
        2
    ) as percent_of_total_expenses
    
FROM categories_category c
JOIN transactions_transaction t ON c.id = t.category_id
WHERE t.type = 'expense'
    AND t.date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY c.id, c.name, c.type, c.color
ORDER BY total_amount DESC
LIMIT 5;