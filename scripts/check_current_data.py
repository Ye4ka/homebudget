#!/usr/bin/env python3
"""
Проверка текущих данных в базе (без внешних зависимостей)
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR, os.path.join(BASE_DIR, 'backend')])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection

def print_separator(text):
    """Печать разделителя."""
    print(f"\n{'='*60}")
    print(f" {text}")
    print('='*60)

def format_table(rows, headers=None):
    """Простое форматирование таблицы."""
    if not rows:
        return "   Нет данных"
    
    result = []
    if headers:
        # Заголовки
        header_line = " | ".join(str(h).ljust(15) for h in headers)
        separator = "-+-".join("-" * 15 for _ in headers)
        result.append(header_line)
        result.append(separator)
    
    # Данные
    for row in rows:
        if isinstance(row, (list, tuple)):
            line = " | ".join(str(cell).ljust(15)[:15] for cell in row)
        else:
            line = str(row)
        result.append(line)
    
    return "\n".join(result)

def check_data_quality():
    """Проверить качество данных."""
    print_separator("ПРОВЕРКА КАЧЕСТВА ДАННЫХ")
    
    checks = [
        ("Пользователи без email",
         "SELECT id, username FROM users_user WHERE email IS NULL OR email = '';"),
        
        ("Бюджеты без владельца",
         "SELECT id, name FROM budgets_budget WHERE owner_id NOT IN (SELECT id FROM users_user);"),
        
        ("Транзакции с отрицательной суммой",
         "SELECT id, amount FROM transactions_transaction WHERE amount <= 0;"),
        
        ("Транзакции без категории",
         "SELECT id, budget_id FROM transactions_transaction WHERE category_id IS NULL;"),
        
        ("Категории без типа",
         "SELECT id, name FROM categories_category WHERE type NOT IN ('income', 'expense');"),
    ]
    
    with connection.cursor() as cursor:
        for check_name, sql in checks:
            cursor.execute(sql)
            results = cursor.fetchall()
            
            if results:
                print(f"\n  {check_name}: {len(results)} проблем")
                print(format_table(results[:5]))  # Показываем первые 5
            else:
                print(f" {check_name}: OK")

def show_sample_data():
    """Показать примеры данных."""
    print_separator("ПРИМЕРЫ ДАННЫХ")
    
    queries = [
        (" Пользователи", 
         "SELECT id, username, email, currency FROM users_user LIMIT 5;"),
        
        (" Бюджеты",
         "SELECT b.id, b.name, b.type, b.currency, u.username as owner FROM budgets_budget b JOIN users_user u ON b.owner_id = u.id LIMIT 5;"),
        
        ("  Категории",
         "SELECT id, name, type, color FROM categories_category LIMIT 5;"),
        
        (" Транзакции",
         "SELECT t.id, t.date, t.type, t.amount, c.name as category FROM transactions_transaction t JOIN categories_category c ON t.category_id = c.id ORDER BY t.date DESC LIMIT 5;"),
    ]
    
    with connection.cursor() as cursor:
        for title, sql in queries:
            print(f"\n{title}:")
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            print(format_table(rows, columns))

def show_table_counts():
    """Показать количество записей в таблицах."""
    print_separator("СТАТИСТИКА ТАБЛИЦ")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                'users_user' as table_name, COUNT(*) as count FROM users_user
            UNION ALL
            SELECT 'budgets_budget', COUNT(*) FROM budgets_budget
            UNION ALL
            SELECT 'categories_category', COUNT(*) FROM categories_category
            UNION ALL
            SELECT 'transactions_transaction', COUNT(*) FROM transactions_transaction
            UNION ALL
            SELECT 'budgets_budgetmember', COUNT(*) FROM budgets_budgetmember
            ORDER BY count DESC;
        """)
        
        rows = cursor.fetchall()
        print("\n Количество записей:")
        for table, count in rows:
            print(f"  {table:25} {count:10} записей")

def show_table_structure():
    """Показать структуру ключевых таблиц."""
    print_separator("СТРУКТУРА ТАБЛИЦ")
    
    tables = ['users_user', 'budgets_budget', 'categories_category', 'transactions_transaction']
    
    with connection.cursor() as cursor:
        for table in tables:
            print(f"\n {table}:")
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table}'
                ORDER BY ordinal_position;
            """)
            
            rows = cursor.fetchall()
            if rows:
                for col_name, data_type, nullable in rows:
                    null_text = "NULL" if nullable == 'YES' else "NOT NULL"
                    print(f"  {col_name:20} {data_type:20} {null_text}")
            else:
                print("  Таблица не найдена")

def check_indexes():
    """Проверить существующие индексы."""
    print_separator("СУЩЕСТВУЮЩИЕ ИНДЕКСЫ")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = 'public'
                AND tablename IN (
                    'users_user',
                    'budgets_budget', 
                    'categories_category',
                    'transactions_transaction'
                )
            ORDER BY tablename, indexname;
        """)
        
        rows = cursor.fetchall()
        
        if rows:
            current_table = None
            for table, index, definition in rows:
                if table != current_table:
                    print(f"\n📁 {table}:")
                    current_table = table
                print(f"  🔸 {index}")
                # Обрезаем длинное определение
                if len(definition) > 80:
                    print(f"    {definition[:80]}...")
                else:
                    print(f"    {definition}")
        else:
            print(" Нет индексов в ключевых таблицах")

def main():
    """Основная функция."""
    print(" ПРОВЕРКА ТЕКУЩЕЙ БАЗЫ ДАННЫХ HomeBudget")
    print("="*70)
    
    show_table_counts()
    show_sample_data()
    check_data_quality()
    show_table_structure()
    check_indexes()
    
    print("\n" + "="*70)
    print(" ПРОВЕРКА ЗАВЕРШЕНА")
    print("="*70)

if __name__ == '__main__':
    main()