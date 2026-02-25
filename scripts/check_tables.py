from django.db import connection
from django.apps import apps

def check_table_structure():
    """Проверка структуры таблиц новых моделей."""
    
    models_to_check = [
        ('budgets', 'Budget'),
        ('categories', 'Category'),
        ('transactions', 'Transaction'),
        ('users', 'User'),
    ]
    
    with connection.cursor() as cursor:
        for app_label, model_name in models_to_check:
            try:
                model = apps.get_model(app_label, model_name)
                table_name = model._meta.db_table
                
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """)
                
                columns = cursor.fetchall()
                print(f"\n{table_name} ({len(columns)} колонок):")
                
                for col in columns:
                    print(f"  {col[0]:30} {col[1]:20} {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
                    
            except Exception as e:
                print(f"Ошибка при проверке {model_name}: {e}")