# СПРАВОЧНИК ТАБЛИЦ БАЗЫ ДАННЫХ

## ОБЗОР
Документ содержит полное описание всех таблиц базы данных HomeBudget.

## ТАБЛИЦА: users_user (Пользователи)

### Назначение
Хранение данных пользователей приложения.

### Структура
| Поле | Тип | Null | По умолчанию | Описание |
|------|-----|------|--------------|----------|
| id | SERIAL | NO | | Первичный ключ |
| password | VARCHAR(128) | NO | | Хеш пароля (Django) |
| last_login | TIMESTAMPTZ | YES | NULL | Дата последнего входа |
| is_superuser | BOOLEAN | NO | false | Флаг суперпользователя |
| username | VARCHAR(150) | NO | | Уникальное имя пользователя |
| first_name | VARCHAR(150) | YES | '' | Имя |
| last_name | VARCHAR(150) | YES | '' | Фамилия |
| email | VARCHAR(254) | NO | | Электронная почта |
| is_staff | BOOLEAN | NO | false | Флаг персонала |
| is_active | BOOLEAN | NO | true | Активен ли пользователь |
| date_joined | TIMESTAMPTZ | NO | CURRENT_TIMESTAMP | Дата регистрации |
| currency | VARCHAR(3) | NO | 'RUB' | Валюта по умолчанию |

### Индексы
- `users_user_pkey` (PRIMARY KEY) на `id`
- `users_user_username_key` (UNIQUE) на `username`
- `users_user_email_key` (UNIQUE) на `email`

### Ограничения
- `CHECK` длина username >= 1
- `CHECK` email соответствует формату

### Пример данных
```sql
INSERT INTO users_user (username, email, password, currency) 
VALUES ('ivanov', 'ivanov@example.com', 'pbkdf2_sha256$...', 'RUB');
ТАБЛИЦА: budgets_budget (Бюджеты)
Назначение
Хранение бюджетов пользователей (личные и семейные).

Структура
Поле	Тип	Null	По умолчанию	Описание
id	SERIAL	NO		Первичный ключ
name	VARCHAR(100)	NO		Название бюджета
type	VARCHAR(20)	NO		Тип: 'personal' или 'family'
owner_id	INTEGER	NO		Владелец (FK → users_user.id)
created_at	TIMESTAMPTZ	NO	CURRENT_TIMESTAMP	Дата создания
currency	VARCHAR(3)	NO	'RUB'	Валюта бюджета
Индексы
budgets_budget_pkey (PRIMARY KEY) на id

budgets_budget_owner_id (FOREIGN KEY) на owner_id

Ограничения
CHECK type IN ('personal', 'family')

CHECK длина name >= 1

FOREIGN KEY owner_id REFERENCES users_user(id) ON DELETE CASCADE

Пример данных
sql
INSERT INTO budgets_budget (name, type, owner_id, currency)
VALUES ('Личный бюджет', 'personal', 1, 'RUB');
ТАБЛИЦА: categories_category (Категории)
Назначение
Хранение категорий доходов и расходов.

Структура
Поле	Тип	Null	По умолчанию	Описание
id	SERIAL	NO		Первичный ключ
name	VARCHAR(100)	NO		Название категории
type	VARCHAR(10)	NO		Тип: 'income' или 'expense'
color	VARCHAR(7)	NO	'#3498db'	Цвет в HEX формате
icon	VARCHAR(50)	YES	NULL	Иконка (FontAwesome класс)
is_default	BOOLEAN	NO	false	Стандартная категория
budget_id	INTEGER	YES	NULL	Бюджет (FK → budgets_budget.id)
created_by	INTEGER	YES	NULL	Создатель (FK → users_user.id)
Индексы
categories_category_pkey (PRIMARY KEY) на id

categories_category_budget_id (FOREIGN KEY) на budget_id

categories_category_created_by (FOREIGN KEY) на created_by

Ограничения
CHECK type IN ('income', 'expense')

CHECK color LIKE '#______'

FOREIGN KEY budget_id REFERENCES budgets_budget(id) ON DELETE SET NULL

FOREIGN KEY created_by REFERENCES users_user(id) ON DELETE SET NULL

Стандартные категории
sql
-- Доходы
('Зарплата', 'income', '#2ecc71', 'money-bill', true),
('Фриланс', 'income', '#27ae60', 'laptop-code', true),
('Инвестиции', 'income', '#16a085', 'chart-line', true),

-- Расходы
('Продукты', 'expense', '#e74c3c', 'shopping-cart', true),
('Транспорт', 'expense', '#f39c12', 'car', true),
('Развлечения', 'expense', '#9b59b6', 'film', true);
ТАБЛИЦА: transactions_transaction (Транзакции)
Назначение
Хранение всех финансовых операций (доходы и расходы).

Структура
Поле	Тип	Null	По умолчанию	Описание
id	SERIAL	NO		Первичный ключ
amount	DECIMAL(10,2)	NO		Сумма транзакции
type	VARCHAR(10)	NO		Тип: 'income' или 'expense'
description	TEXT	YES	''	Описание транзакции
date	DATE	NO	CURRENT_DATE	Дата транзакции
category_id	INTEGER	NO		Категория (FK → categories_category.id)
budget_id	INTEGER	NO		Бюджет (FK → budgets_budget.id)
created_by	INTEGER	NO		Создатель (FK → users_user.id)
created_at	TIMESTAMPTZ	NO	CURRENT_TIMESTAMP	Дата создания записи
Индексы
transactions_transaction_pkey (PRIMARY KEY) на id

idx_transaction_budget_date на budget_id, date DESC

idx_transaction_budget_category на budget_id, category_id

idx_transaction_type на type

transactions_transaction_category_id (FOREIGN KEY) на category_id

transactions_transaction_budget_id (FOREIGN KEY) на budget_id

transactions_transaction_created_by (FOREIGN KEY) на created_by

Ограничения
CHECK amount > 0

CHECK type IN ('income', 'expense')

CHECK date <= CURRENT_DATE

FOREIGN KEY category_id REFERENCES categories_category(id) ON DELETE RESTRICT

FOREIGN KEY budget_id REFERENCES budgets_budget(id) ON DELETE CASCADE

FOREIGN KEY created_by REFERENCES users_user(id) ON DELETE CASCADE

Пример данных
sql
INSERT INTO transactions_transaction 
(amount, type, description, date, category_id, budget_id, created_by)
VALUES 
(50000.00, 'income', 'Зарплата за декабрь', '2024-12-15', 1, 1, 1),
(2500.50, 'expense', 'Покупки в супермаркете', '2024-12-16', 4, 1, 1);
СВЯЗИ МЕЖДУ ТАБЛИЦАМИ
Диаграмма связей
text
users_user
    │
    ├── budgets_budget (owner_id → id)
    │       │
    │       ├── categories_category (budget_id → id)
    │       │       │
    │       └── transactions_transaction (budget_id → id)
    │               │
    │               └── categories_category (category_id → id)
    │
    ├── categories_category (created_by → id)
    │
    └── transactions_transaction (created_by → id)
Типы связей
One-to-Many:

User → Budgets (1 пользователь → N бюджетов)

Budget → Transactions (1 бюджет → N транзакций)

Category → Transactions (1 категория → N транзакций)

Many-to-Many:

User ↔ Budget (через BudgetMember - не реализовано в текущей схеме)

СТАТИСТИКА ТАБЛИЦ
Текущие размеры
sql
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size('public.' || tablename)) as total_size,
    pg_size_pretty(pg_relation_size('public.' || tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size('public.' || tablename) - 
                   pg_relation_size('public.' || tablename)) as index_size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size('public.' || tablename) DESC;
Оценка роста
users_user: ~100 КБ на 1000 пользователей

transactions_transaction: ~10 МБ на 100,000 транзакций

budgets_budget: ~50 КБ на 1000 бюджетов

categories_category: ~10 КБ на 100 категорий

ОПЕРАЦИИ ОБСЛУЖИВАНИЯ
Очистка старых данных
sql
-- Архивация транзакций старше 3 лет
CREATE TABLE transactions_archive AS 
SELECT * FROM transactions_transaction 
WHERE date < CURRENT_DATE - INTERVAL '3 years';

DELETE FROM transactions_transaction 
WHERE date < CURRENT_DATE - INTERVAL '3 years';
Перестроение индексов
sql
-- Ежемесячное обслуживание
REINDEX TABLE transactions_transaction;
VACUUM ANALYZE transactions_transaction;
Дата создания: 17.12.2024
Версия: 1.0
Обновление: При изменении структуры БД
Ответственный: Администратор БД HomeBudget