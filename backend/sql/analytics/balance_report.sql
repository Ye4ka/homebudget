-- Отчет по балансу бюджетов
SELECT 
    bs.budget_name,
    bs.budget_type,
    bs.currency,
    bs.owner_username,
    bs.transaction_count,
    bs.total_income,
    bs.total_expense,
    bs.balance,
    CASE 
        WHEN bs.total_expense > 0 
        THEN ROUND((bs.total_income / bs.total_expense) * 100, 2)
        ELSE 100 
    END as income_expense_ratio,
    bs.first_transaction,
    bs.last_transaction
FROM budget_summary bs
ORDER BY bs.balance DESC;