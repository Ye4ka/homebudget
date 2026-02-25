-- 4. Сравнение доходов/расходов по месяцам
WITH monthly_data AS (
    SELECT 
        DATE_TRUNC('month', t.date)::DATE as month_start,
        EXTRACT(YEAR FROM t.date) as year,
        EXTRACT(MONTH FROM t.date) as month_number,
        TO_CHAR(t.date, 'Month') as month_name,
        
        COUNT(t.id) as transaction_count,
        SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END) as monthly_income,
        SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END) as monthly_expense,
        SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE -t.amount END) as monthly_balance,
        
        COUNT(DISTINCT t.budget_id) as active_budgets,
        COUNT(DISTINCT t.category_id) as used_categories
    FROM transactions_transaction t
    WHERE t.date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '6 months')
    GROUP BY DATE_TRUNC('month', t.date), EXTRACT(YEAR FROM t.date), EXTRACT(MONTH FROM t.date)
)
SELECT 
    month_start,
    year,
    month_number,
    TRIM(month_name) as month_name,
    
    transaction_count,
    monthly_income,
    monthly_expense,
    monthly_balance,
    
    active_budgets,
    used_categories,
    
    -- Процентные изменения
    ROUND(
        (monthly_income - LAG(monthly_income, 1) OVER (ORDER BY month_start)) * 100.0 / 
        NULLIF(LAG(monthly_income, 1) OVER (ORDER BY month_start), 0), 
        2
    ) as income_growth_percent,
    
    ROUND(
        (monthly_expense - LAG(monthly_expense, 1) OVER (ORDER BY month_start)) * 100.0 / 
        NULLIF(LAG(monthly_expense, 1) OVER (ORDER BY month_start), 0), 
        2
    ) as expense_growth_percent,
    
    -- Отношение доходов к расходам
    CASE 
        WHEN monthly_expense > 0 
        THEN ROUND((monthly_income / monthly_expense) * 100, 2)
        ELSE 100 
    END as income_expense_ratio
    
FROM monthly_data
ORDER BY month_start DESC;