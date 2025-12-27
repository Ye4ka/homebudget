import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def check_all_tables():
    print("Проверка всех таблиц в БД")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Все таблицы проекта
        expected_tables = [
            'users', 'budgets', 'budget_members',
            'categories', 'transactions', 'budget_limits',
            'financial_goals', 'notifications'
        ]
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"Таблиц в БД: {len(existing_tables)}")
        print("-" * 40)
        
        for table in expected_tables:
            if table in existing_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f" {table:20} | {count:4} записей")
            else:
                print(f" {table:20} | ОТСУТСТВУЕТ в БД!")
        
        print("=" * 60)
        
        if len(existing_tables) == len(expected_tables):
            print("Все таблицы созданы правильно")
            return True
        else:
            print("Некоторые таблицы отсутствуют")
            return False

if __name__ == "__main__":
    success = check_all_tables()
    sys.exit(0 if success else 1)