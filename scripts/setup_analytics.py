
"""
Полная настройка аналитики для текущей базы
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR, os.path.join(BASE_DIR, 'backend')])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection

def print_step(step, description):
    """Печать шага выполнения."""
    print(f"\n {step}. {description}")
    print("-" * 50)

def execute_sql(sql, description=None):
    """Выполнить SQL запрос."""
    if description:
        print(f"  {description}...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if cursor.description:  # Если есть результат
                rows = cursor.fetchall()
                if rows:
                    print(f"     Результат: {len(rows)} строк")
                    return rows
        print(f"     Выполнено")
        return True
    except Exception as e:
        error_msg = str(e)
        if "already exists" in error_msg:
            print(f"    ⏭  Уже существует")
        else:
            print(f"     Ошибка: {error_msg[:100]}")
        return False

def create_indexes():
    """Создать индексы для оптимизации."""
    print_step(1, "СОЗДАНИЕ ИНДЕКСОВ")
    
    indexes = [
        ("idx_transaction_budget_date", 
         "CREATE INDEX IF NOT EXISTS idx_transaction_budget_date ON transactions_transaction (budget_id, date DESC)"),
        
        ("idx_transaction_budget_category",
         "CREATE INDEX IF NOT EXISTS idx_transaction_budget_category ON transactions_transaction (budget_id, category_id)"),
        
        ("idx_transaction_type",
         "CREATE INDEX IF NOT EXISTS idx_transaction_type ON transactions_transaction (type)"),
        
        ("idx_transaction_date",
         "CREATE INDEX IF NOT EXISTS idx_transaction_date ON transactions_transaction (date)"),
        
        ("idx_budget_owner",
         "CREATE INDEX IF NOT EXISTS idx_budget_owner ON budgets_budget (owner_id)"),
        
        ("idx_budget_type", 
         "CREATE INDEX IF NOT EXISTS idx_budget_type ON budgets_budget (type)"),
        
        ("idx_category_type",
         "CREATE INDEX IF NOT EXISTS idx_category_type ON categories_category (type)"),
        
        ("idx_user_email",
         "CREATE INDEX IF NOT EXISTS idx_user_email ON users_user (email)"),
    ]
    
    for idx_name, sql in indexes:
        execute_sql(sql, f"Создание индекса {idx_name}")

def create_views():
    """Создать аналитические представления."""
    print_step(2, "СОЗДАНИЕ АНАЛИТИЧЕСКИХ ПРЕДСТАВЛЕНИЙ")
    
    # 1. Удалить старый материализованный view если есть
    execute_sql("DROP MATERIALIZED VIEW IF EXISTS monthly_summary;", 
                "Удаление старого monthly_summary")
    
    # 2. Создать представление бюджетов
    execute_sql("""
        CREATE OR REPLACE VIEW budget_summary AS
        SELECT 
            b.id,
            b.name as budget_name,
            b.type as budget_type,
            b.currency,
            u.username as owner_username,
            u.email as owner_email,
            COUNT(t.id) as transaction_count,
            COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
            COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expense,
            COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE -t.amount END), 0) as balance,
            MIN(t.date) as first_transaction,
            MAX(t.date) as last_transaction
        FROM budgets_budget b
        JOIN users_user u ON b.owner_id = u.id
        LEFT JOIN transactions_transaction t ON b.id = t.budget_id
        GROUP BY b.id, b.name, b.type, b.currency, u.username, u.email;
    """, "Создание budget_summary")
    
    # 3. Создать представление категорий
    execute_sql("""
        CREATE OR REPLACE VIEW category_summary AS
        SELECT 
            c.id,
            c.name as category_name,
            c.type as category_type,
            c.color,
            c.icon,
            COUNT(t.id) as transaction_count,
            COALESCE(SUM(t.amount), 0) as total_amount,
            COALESCE(AVG(t.amount), 0) as average_amount,
            MIN(t.date) as first_transaction,
            MAX(t.date) as last_transaction,
            COUNT(DISTINCT t.budget_id) as budget_count
        FROM categories_category c
        LEFT JOIN transactions_transaction t ON c.id = t.category_id
        GROUP BY c.id, c.name, c.type, c.color, c.icon;
    """, "Создание category_summary")
    
    # 4. Создать материализованное представление месячной статистики
    execute_sql("""
        CREATE MATERIALIZED VIEW monthly_summary AS
        SELECT 
            DATE_TRUNC('month', t.date)::DATE as month_start,
            EXTRACT(YEAR FROM t.date) as year,
            EXTRACT(MONTH FROM t.date) as month,
            COUNT(t.id) as transaction_count,
            COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
            COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expense,
            COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE -t.amount END), 0) as balance,
            COUNT(DISTINCT t.budget_id) as budget_count,
            COUNT(DISTINCT t.category_id) as category_count
        FROM transactions_transaction t
        WHERE t.date IS NOT NULL
        GROUP BY DATE_TRUNC('month', t.date), EXTRACT(YEAR FROM t.date), EXTRACT(MONTH FROM t.date)
        ORDER BY year DESC, month DESC;
    """, "Создание monthly_summary")
    
    # 5. Создать индекс для monthly_summary
    execute_sql("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_monthly_summary_date 
        ON monthly_summary (month_start);
    """, "Создание индекса для monthly_summary")
    
    # 6. Создать функцию обновления
    execute_sql("""
        CREATE OR REPLACE FUNCTION refresh_monthly_summary()
        RETURNS void AS $$
        BEGIN
            REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_summary;
        END;
        $$ LANGUAGE plpgsql;
    """, "Создание функции refresh_monthly_summary")

def test_views():
    """Протестировать созданные представления."""
    print_step(3, "ТЕСТИРОВАНИЕ ПРЕДСТАВЛЕНИЙ")
    
    test_queries = [
        ("Проверка budget_summary", 
         "SELECT budget_name, currency, balance FROM budget_summary ORDER BY balance DESC LIMIT 3;"),
        
        ("Проверка category_summary (расходы)", 
         "SELECT category_name, total_amount FROM category_summary WHERE category_type = 'expense' ORDER BY total_amount DESC LIMIT 3;"),
        
        ("Проверка category_summary (доходы)", 
         "SELECT category_name, total_amount FROM category_summary WHERE category_type = 'income' ORDER BY total_amount DESC LIMIT 3;"),
        
        ("Проверка monthly_summary", 
         "SELECT month_start, transaction_count, total_income, total_expense FROM monthly_summary ORDER BY month_start DESC LIMIT 3;"),
    ]
    
    for description, sql in test_queries:
        print(f"\n   {description}:")
        rows = execute_sql(sql)
        if rows and isinstance(rows, list):
            for row in rows[:3]:  # Показываем первые 3 результата
                print(f"    {row}")

def show_database_info():
    """Показать информацию о базе."""
    print_step(4, "ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ")
    
    # Показать существующие представления
    execute_sql("""
        SELECT table_name, table_type 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
            AND table_type IN ('VIEW', 'MATERIALIZED VIEW')
        ORDER BY table_type, table_name;
    """, "Существующие представления")
    
    # Показать размеры таблиц
    execute_sql("""
        SELECT 
            table_name,
            pg_size_pretty(pg_total_relation_size(table_name)) as size
        FROM information_schema.tables
        WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        ORDER BY pg_total_relation_size(table_name) DESC
        LIMIT 5;
    """, "Размеры таблиц")

def main():
    """Основная функция."""
    print(" ПОЛНАЯ НАСТРОЙКА АНАЛИТИКИ ДЛЯ HOMEBUDGET")
    print("="*60)
    
    create_indexes()
    create_views()
    test_views()
    show_database_info()
    
    print("\n" + "="*60)
    print(" НАСТРОЙКА ЗАВЕРШЕНА!")
    print("="*60)
    print("\n ИСПОЛЬЗОВАНИЕ:")
    print("  1. SELECT * FROM budget_summary;")
    print("  2. SELECT * FROM category_summary WHERE category_type = 'expense';")
    print("  3. SELECT * FROM monthly_summary;")
    print("  4. SELECT refresh_monthly_summary(); -- для обновления")

if __name__ == '__main__':
    main()