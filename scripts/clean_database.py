#!/usr/bin/env python3
"""
Очистка базы данных от старых данных
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR, os.path.join(BASE_DIR, 'backend')])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection

def clean_database():
    """Очистить все таблицы в правильном порядке."""
    print("🧹 ОЧИСТКА БАЗЫ ДАННЫХ")
    print("="*50)
    
    # Порядок удаления (от дочерних к родительским)
    tables = [
        # Сначала все таблицы с внешними ключами
        'transactions_transaction',
        'budgets_budgetmember',  # старая таблица
        'budgets_budget',
        'categories_category',
        'users_user',
        
        # Django системные таблицы (опционально)
        'django_admin_log',
        'django_session',
    ]
    
    with connection.cursor() as cursor:
        # Отключаем проверку внешних ключей
        cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
        
        for table in tables:
            try:
                cursor.execute(f"DELETE FROM {table};")
                print(f"✅ Очищена таблица: {table}")
            except Exception as e:
                print(f"⚠️  Не удалось очистить {table}: {e}")
        
        # Включаем обратно
        cursor.execute("SET CONSTRAINTS ALL IMMEDIATE;")
    
    print("\n✅ База данных очищена!")

if __name__ == '__main__':
    response = input("⚠️  Это удалит ВСЕ данные из базы. Продолжить? (y/N): ").strip().lower()
    if response == 'y':
        clean_database()
    else:
        print("Отменено")