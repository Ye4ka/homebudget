# 📊 ДОКУМЕНТАЦИЯ ПО ИНДЕКСАМ

## СОСТАВНЫЕ ИНДЕКСЫ

### Транзакции:
- `idx_budget_date` (budget_id, date DESC) - история транзакций
- `idx_budget_category` (budget_id, category_id) - статистика по категориям  
- `idx_trans_type` (type) - фильтрация по типу

### Уведомления:
- `idx_user_read` (user_id, is_read) - непрочитанные уведомления
- `idx_created_at_desc` (created_at DESC) - сортировка по времени

## ПРОВЕРКА (15.12.2024):
✅ Все индексы созданы успешно