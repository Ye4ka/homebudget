# АРХИТЕКТУРА БАЗЫ ДАННЫХ HOMEBUDGET

## ОБЗОР
Документ описывает структуру, связи и принципы работы базы данных HomeBudget.

## ТЕХНОЛОГИЧЕСКИЙ СТЕК
- **СУБД:** PostgreSQL 18.1
- **Кодировка:** UTF-8
- **Локаль:** С
- **Расширения:** pg_stat_statements (мониторинг)

## ФИЗИЧЕСКАЯ СТРУКТУРА

### Табличные пространства
```sql
-- Основные таблицы
SET default_tablespace = '';

-- Индексы
CREATE TABLESPACE idxspace LOCATION '/var/lib/postgresql/18.1/data/indexes';
Параметры PostgreSQL (postgresql.conf)
text
shared_buffers = 128MB
work_mem = 4MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
ЛОГИЧЕСКАЯ СТРУКТУРА
1. Схема public
Основная схема приложения содержит все таблицы приложения.

2. Схема analytics (опционально)
Для аналитических представлений и материализованных представлений.

ПРИНЦИПЫ ПРОЕКТИРОВАНИЯ
Нормализация
1NF: Все поля атомарны

2NF: Зависимость от первичного ключа

3NF: Транзитивные зависимости устранены

Денормализация (для производительности)
Поле type в таблице transactions_transaction (дублирует category.type)

Поле currency в budgets_budget (для быстрого доступа)

Соглашения об именовании
Таблицы: множественное число (users, transactions)

Первичные ключи: id

Внешние ключи: {table_name}_id

Индексы: idx_{table}_{columns}_{suffix}

МИГРАЦИИ
Стратегия миграций
Backward compatible изменения

Неразрушающие изменения (ALTER TABLE ADD COLUMN)

Поэтапное развертывание

Миграционные скрипты
text
backend/apps/
├── users/migrations/
├── budgets/migrations/
├── categories/migrations/
└── transactions/migrations/
БЕЗОПАСНОСТЬ
Роли и привилегии
sql
-- Основная роль приложения
CREATE ROLE homebudget_app LOGIN PASSWORD 'secure_password';

-- Только чтение для отчетов
CREATE ROLE homebudget_readonly LOGIN PASSWORD 'readonly_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO homebudget_readonly;

-- Административная роль
CREATE ROLE homebudget_admin WITH CREATEDB CREATEROLE;
Шифрование данных
Пароли: bcrypt (через Django)

Конфиденциальные данные: могут быть зашифрованы на уровне приложения

ПРОИЗВОДИТЕЛЬНОСТЬ
Стратегия индексирования
Составные индексы для частых запросов

Частичные индексы для активных данных

Индексы выражения для вычисляемых полей

Партиционирование
-- Для больших объемов данных (транзакции)
CREATE TABLE transactions_transaction_2024 PARTITION OF transactions_transaction
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
РЕПЛИКАЦИЯ И РЕЗЕРВИРОВАНИЕ
Стратегия резервного копирования
Ежедневно: Полный backup

Еженедельно: Проверка восстановления

Хранение: 7 дней локально, 30 дней в облаке

Репликация (опционально)
Master-Slave для отчетов

Read replicas для высокой нагрузки

СХЕМА РАЗВЕРТЫВАНИЯ
Development
text
PostgreSQL 15 на localhost
Без репликации
Минимальные ресурсы
Production
text
PostgreSQL 18.1 кластер
Master + 2 Replicas
Автоматическое резервное копирование
Мониторинг и алертинг
