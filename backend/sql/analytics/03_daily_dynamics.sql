-- 3. Динамика баланса по дням с оконными функциями
WITH daily_stats AS (
    SELECT 
        t.date,
        COUNT(t.id) as daily_transactions,
        SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END) as daily_income,
        SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END) as daily_expense,
        SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE -t.amount END) as daily_balance
    FROM transactions_transaction t
    WHERE t.date BETWEEN '2024-01-01' AND '2024-01-31'
    GROUP BY t.date
)
SELECT 
    date,
    daily_transactions,
    daily_income,
    daily_expense,
    daily_balance,
    
    -- Накопительный баланс
    SUM(daily_balance) OVER (ORDER BY date) as cumulative_balance,
    
    -- Средние за 7 дней
    ROUND(AVG(daily_income) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) as avg_income_7d,
    ROUND(AVG(daily_expense) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) as avg_expense_7d,
    
    -- Тренд (разница с предыдущим днем)
    daily_balance - LAG(daily_balance, 1) OVER (ORDER BY date) as balance_change,
    
    -- День недели для анализа
    TO_CHAR(date, 'Day') as day_of_week,
    EXTRACT(DOW FROM date) as day_of_week_num
    
FROM daily_stats
ORDER BY date;