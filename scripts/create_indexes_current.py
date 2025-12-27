#!/usr/bin/env python3
"""
Создание индексов для текущей структуры базы
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR, os.path.join(BASE_DIR, 'backend')])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection

def create_indexes():
    """Создать индексы для оптимизации запросов."""
    
    print(" СОЗДАНИЕ ИНДЕКСОВ ДЛЯ ТЕКУЩЕЙ СТРУКТУРЫ")
    print("="*60)
    
    indexes = [
        # Для транзакций (самая важная таблица)
        ("idx_transaction_budget_date", 
         "CREATE INDEX IF NOT EXISTS idx_transaction_budget_date ON transactions_transaction (budget_id, date DESC)"),
        
        ("idx_transaction_budget_category",
         "CREATE INDEX IF NOT EXISTS idx_transaction_budget_category ON transactions_transaction (budget_id, category_id)"),
        
        ("idx_transaction_type",
         "CREATE INDEX IF NOT EXISTS idx_transaction_type ON transactions_transaction (type)"),
        
        ("idx_transaction_date",
         "CREATE INDEX IF NOT EXISTS idx_transaction_date ON transactions_transaction (date)"),
        
        # Для бюджетов
        ("idx_budget_owner",
         "CREATE INDEX IF NOT EXISTS idx_budget_owner ON budgets_budget (owner_id)"),
        
        ("idx_budget_type", 
         "CREATE INDEX IF NOT EXISTS idx_budget_type ON budgets_budget (type)"),
        
        # Для категорий
        ("idx_category_type",
         "CREATE INDEX IF NOT EXISTS idx_category_type ON categories_category (type)"),
        
        # Для пользователей (если часто ищем по email)
        ("idx_user_email",
         "CREATE INDEX IF NOT EXISTS idx_user_email ON users_user (email)"),
    ]
    
    with connection.cursor() as cursor:
        success_count = 0
        error_count = 0
        
        for idx_name, sql in indexes:
            try:
                # Проверяем существование индекса
                cursor.execute(f"""
                    SELECT 1 FROM pg_indexes 
                    WHERE indexname = '{idx_name}' 
                    AND schemaname = 'public';
                """)
                
                if cursor.fetchone():
                    print(f"⏭  Уже существует: {idx_name}")
                else:
                    cursor.execute(sql)
                    print(f" Создан: {idx_name}")
                    success_count += 1
                    
            except Exception as e:
                print(f" Ошибка: {idx_name} - {str(e).split('DETAIL')[0]}")
                error_count += 1
        
        print(f"\n Итог: {success_count} создано, {error_count} ошибок")

def check_existing_indexes():
    """Проверить существующие индексы."""
    print("\n СУЩЕСТВУЮЩИЕ ИНДЕКСЫ")
    print("="*60)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = 'public'
                AND tablename IN (
                    'transactions_transaction',
                    'budgets_budget', 
                    'categories_category',
                    'users_user'
                )
            ORDER BY tablename, indexname;
        """)
        
        indexes = cursor.fetchall()
        
        if indexes:
            for schema, table, name, definition in indexes:
                print(f"\n {table}.{name}:")
                print(f"   {definition[:100]}...")
        else:
            print(" Нет индексов в ключевых таблицах")

def main():
    """Основная функция."""
    check_existing_indexes()
    
    response = input("\nСоздать недостающие индексы? (y/N): ").strip().lower()
    if response == 'y':
        create_indexes()
    else:
        print("Отменено")

if __name__ == '__main__':
    main()