-- Отчет по категориям
SELECT 
    cs.category_name,
    cs.category_type,
    cs.transaction_count,
    cs.total_amount,
    cs.average_amount,
    cs.budget_count,
    cs.first_transaction,
    cs.last_transaction
FROM category_summary cs
WHERE cs.category_type = 'expense'  -- или 'income'
ORDER BY cs.total_amount DESC;