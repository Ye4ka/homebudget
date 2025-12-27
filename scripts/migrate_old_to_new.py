
"""
Миграция данных из старых моделей в новые
"""

import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR, os.path.join(BASE_DIR, 'backend')])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

def migrate_users():
    """Мигрировать пользователей из старой модели в новую."""
    print("👥 Миграция пользователей...")
    
    with connection.cursor() as cursor:
        # 1. Добавить недостающие поля если нужно
        cursor.execute("""
            ALTER TABLE users_user 
            ADD COLUMN IF NOT EXISTS username_new VARCHAR(150),
            ADD COLUMN IF NOT EXISTS date_joined_new TIMESTAMP DEFAULT NOW();
        """)
        
        # 2. Копировать данные из username в email если email пустой
        cursor.execute("""
            UPDATE users_user 
            SET email = username 
            WHERE (email IS NULL OR email = '') AND username IS NOT NULL;
        """)
        
        # 3. Установить email как username для совместимости
        cursor.execute("""
            UPDATE users_user 
            SET username = email 
            WHERE username IS NULL OR username = '';
        """)
    
    print(f" Пользователей: {User.objects.count()}")

def migrate_budgets():
    """Мигрировать бюджеты."""
    print("\n Миграция бюджетов...")
    
    from apps.budgets.models import Budget
    
    with connection.cursor() as cursor:
        # Проверить структуру таблицы
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'budgets_budget' 
            AND column_name IN ('currency', 'type', 'name');
        """)
        
        columns = [row[0] for row in cursor.fetchall()]
        print(f"Существующие колонки: {columns}")
    
    # Создать новые бюджеты если нужно
    for user in User.objects.all():
        if not user.budgets.exists():
            Budget.objects.create(
                name=f"Бюджет {user.username}",
                owner=user,
                type='personal',
                currency='RUB'
            )
            print(f" Создан бюджет для {user.email}")
    
    print(f" Бюджетов: {Budget.objects.count()}")

def check_current_data():
    """Проверить текущие данные."""
    print("\n ПРОВЕРКА ДАННЫХ")
    print("="*50)
    
    with connection.cursor() as cursor:
        # Таблицы и количество записей
        tables = [
            'users_user',
            'budgets_budget', 
            'categories_category',
            'transactions_transaction',
            'budgets_budgetmember'
        ]
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:30} {count:10} записей")
        
        # Проверить структуру users_user
        print("\n Структура users_user:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'users_user'
            ORDER BY ordinal_position;
        """)
        
        for col in cursor.fetchall():
            print(f"  {col[0]:20} {col[1]:20} {'NULL' if col[2]=='YES' else 'NOT NULL'}")

def main():
    """Основная функция."""
    print(" МИГРАЦИЯ ДАННЫХ ИЗ СТАРОЙ СХЕМЫ")
    print("="*60)
    
    check_current_data()
    
    response = input("\nПродолжить миграцию? (y/N): ").strip().lower()
    if response != 'y':
        print("Отменено")
        return
    
    migrate_users()
    migrate_budgets()
    
    print("\n" + "="*60)
    print(" МИГРАЦИЯ ЗАВЕРШЕНА")
    print("="*60)

if __name__ == '__main__':
    main()