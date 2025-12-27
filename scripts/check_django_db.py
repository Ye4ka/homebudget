#!/usr/bin/env python
import os
import sys
import django
from django.db import connection

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("✓ Django настроен")
except Exception as e:
    print(f"✗ Ошибка Django: {e}")
    sys.exit(1)

# Проверяем подключение к БД
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✓ Подключение к PostgreSQL успешно")
        print(f"  Версия PostgreSQL: {version[0]}")
        
        # Проверяем текущую БД
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"  Текущая БД: {db_name}")
        
        # Проверяем таблицы
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        print(f"  Таблиц в БД: {len(tables)}")
        
        if tables:
            print("  Список таблиц:")
            for table in tables:
                print(f"    - {table[0]}")
                
except Exception as e:
    print(f"✗ Ошибка подключения к БД: {e}")
    print("\nВозможные причины:")
    print("1. PostgreSQL не запущен")
    print("2. Неправильные настройки в DATABASE_URL")
    print("3. База данных не создана")
    print("4. Пользователь не имеет прав доступа")