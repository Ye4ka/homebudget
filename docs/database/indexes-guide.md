# РУКОВОДСТВО ПО ИНДЕКСАМ БАЗЫ ДАННЫХ

## ОБЗОР
Документ описывает все индексы базы данных HomeBudget, их назначение и стратегию использования.

## СТРАТЕГИЯ ИНДЕКСИРОВАНИЯ

### Принципы
1. **Индексировать по запросам:** Только часто используемые WHERE/JOIN
2. **Составные индексы:** Для многостолбцовых условий
3. **Частичные индексы:** Для подмножества данных
4. **Мониторинг:** Регулярная проверка эффективности

### Правила
- Один индекс на таблицу для первичного ключа
- Индексы для всех внешних ключей
- Составные индексы для частых комбинаций фильтров
- Избегать избыточных индексов

## ТЕКУЩИЕ ИНДЕКСЫ

### 1. ПЕРВИЧНЫЕ КЛЮЧИ (PRIMARY KEYS)

#### `users_user_pkey`
```sql
CREATE UNIQUE INDEX users_user_pkey ON users_user(id);
Назначение: Гарантирует уникальность идентификаторов пользователей
Столбцы: id
Тип: B-tree, UNIQUE
Размер: ~16 KB на 1000 пользователей

budgets_budget_pkey
sql
CREATE UNIQUE INDEX budgets_budget_pkey ON budgets_budget(id);
Назначение: Уникальность идентификаторов бюджетов
Столбцы: id

categories_category_pkey
sql
CREATE UNIQUE INDEX categories_category_pkey ON categories_category(id);
Назначение: Уникальность идентификаторов категорий

transactions_transaction_pkey
sql
CREATE UNIQUE INDEX transactions_transaction_pkey ON transactions_transaction(id);
Назначение: Уникальность идентификаторов транзакций
Размер: ~4 MB на 100,000 транзакций

2. ИНДЕКСЫ ВНЕШНИХ КЛЮЧЕЙ (FOREIGN KEYS)
budgets_budget_owner_id
sql
CREATE INDEX budgets_budget_owner_id ON budgets_budget(owner_id);
Назначение: Ускорение JOIN между budgets и users
Запросы: SELECT * FROM budgets WHERE owner_id = ?

categories_category_budget_id
sql
CREATE INDEX categories_category_budget_id ON categories_category(budget_id);
Назначение: Поиск категорий по бюджету
Запросы: SELECT * FROM categories WHERE budget_id = ?

categories_category_created_by
sql
CREATE INDEX categories_category_created_by ON categories_category(created_by);
Назначение: Поиск категорий по создателю

transactions_transaction_category_id
sql
CREATE INDEX transactions_transaction_category_id ON transactions_transaction(category_id);
Назначение: JOIN транзакций с категориями
Запросы: SELECT * FROM transactions WHERE category_id = ?

transactions_transaction_budget_id
sql
CREATE INDEX transactions_transaction_budget_id ON transactions_transaction(budget_id);
Назначение: Поиск транзакций по бюджету
Размер: ~3 MB на 100,000 транзакций

transactions_transaction_created_by
sql
CREATE INDEX transactions_transaction_created_by ON transactions_transaction(created_by);
Назначение: Поиск транзакций по создателю

3. СОСТАВНЫЕ ИНДЕКСЫ
idx_transaction_budget_date
sql
CREATE INDEX idx_transaction_budget_date 
ON transactions_transaction(budget_id, date DESC);
Назначение: Ускорение выборки транзакций по бюджету с сортировкой по дате
Запросы:

sql
-- Основной сценарий
SELECT * FROM transactions_transaction 
WHERE budget_id = 1 
ORDER BY date DESC 
LIMIT 50;

-- Фильтрация по диапазону дат
SELECT * FROM transactions_transaction 
WHERE budget_id = 1 AND date BETWEEN '2024-12-01' AND '2024-12-31';
Размер: ~5 MB на 100,000 транзакций
Covering: Покрывает запросы с budget_id + date

idx_transaction_budget_category
sql
CREATE INDEX idx_transaction_budget_category 
ON transactions_transaction(budget_id, category_id);
Назначение: Аналитика по категориям в рамках бюджета
Запросы:

sql
-- Сумма по категории в бюджете
SELECT SUM(amount) FROM transactions_transaction 
WHERE budget_id = 1 AND category_id = 5;

-- Статистика по категориям
SELECT category_id, COUNT(*), SUM(amount) 
FROM transactions_transaction 
WHERE budget_id = 1 
GROUP BY category_id;
idx_transaction_type
sql
CREATE INDEX idx_transaction_type 
ON transactions_transaction(type);
Назначение: Быстрая фильтрация по типу транзакции
Запросы: SELECT * FROM transactions WHERE type = 'income'
Cardinality: Низкая (2 значения)

4. УНИКАЛЬНЫЕ ИНДЕКСЫ
users_user_username_key
sql
CREATE UNIQUE INDEX users_user_username_key ON users_user(username);
Назначение: Гарантирует уникальность имен пользователей

users_user_email_key
sql
CREATE UNIQUE INDEX users_user_email_key ON users_user(email);
Назначение: Гарантирует уникальность email

АНАЛИЗ ЭФФЕКТИВНОСТИ ИНДЕКСОВ
Мониторинг использования
sql
-- Самые используемые индексы
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;

-- Неиспользуемые индексы
SELECT 
    schemaname,
    tablename,
    indexname
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;
Размеры индексов
sql
SELECT 
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as size
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexname::regclass) DESC;
РЕКОМЕНДАЦИИ ПО ОПТИМИЗАЦИИ
1. Для таблицы transactions_transaction
Добавить частичный индекс для активных данных:
sql
CREATE INDEX idx_transactions_recent 
ON transactions_transaction(budget_id, date DESC) 
WHERE date >= CURRENT_DATE - INTERVAL '90 days';
Индекс для поиска по описанию (если нужно):
sql
CREATE INDEX idx_transactions_description 
ON transactions_transaction USING gin(to_tsvector('russian', description));
2. Для таблицы users_user
Индекс для поиска по имени:
sql
CREATE INDEX idx_users_name 
ON users_user(LOWER(first_name || ' ' || last_name));
3. Для аналитических запросов
Составной индекс для отчетов:
sql
CREATE INDEX idx_analytics_budget_date_type 
ON transactions_transaction(budget_id, date, type);
ПРОФИЛИРОВАНИЕ ЗАПРОСОВ
Проверка плана выполнения
sql
-- Для конкретного запроса
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM transactions_transaction 
WHERE budget_id = 1 
ORDER BY date DESC 
LIMIT 50;
Статистика по индексам
sql
-- Эффективность индексов
SELECT 
    relname as table_name,
    indexrelname as index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    idx_scan as scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched,
    100.0 * idx_tup_fetch / GREATEST(idx_tup_read, 1) as hit_rate
FROM pg_stat_user_indexes 
ORDER BY hit_rate DESC;
ОБСЛУЖИВАНИЕ ИНДЕКСОВ
Перестроение индексов
sql
-- Для фрагментированных индексов
REINDEX INDEX idx_transaction_budget_date;
-- Или для всей таблицы
REINDEX TABLE transactions_transaction;
Обновление статистики
sql
-- После больших изменений данных
ANALYZE transactions_transaction;
-- Принудительное обновление
VACUUM ANALYZE transactions_transaction;
Мониторинг фрагментации
sql
-- Проверка bloat (раздутие) индексов
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    pg_size_pretty(pg_relation_size(indexrelid) - 
                   pg_table_size(indexrelid)) as wasted_space
FROM pg_stat_user_indexes 
WHERE pg_relation_size(indexrelid) > 1000000  -- больше 1MB
ORDER BY wasted_space DESC;
РОСТ ИНДЕКСОВ
Прогноз роста
Таблица	Индекс	Текущий размер	Рост на 100K записей
transactions	pkey	4 MB	+4 MB
transactions	budget_id	3 MB	+3 MB
transactions	budget_date	5 MB	+5 MB
Рекомендации по мониторингу
Еженедельно: Проверять неиспользуемые индексы

Ежемесячно: Анализировать эффективность

Ежеквартально: Перестраивать фрагментированные индексы

При росте данных: Пересматривать стратегию индексирования

Дата создания: 17.12.2024
Версия: 1.0
Обновление: При изменении структуры или добавлении новых индексов
Ответственный: Администратор БД HomeBudget