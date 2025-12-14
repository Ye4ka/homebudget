#!/usr/bin/env python
"""
Скрипт для исправления состояния миграций в базе данных
"""
import os
import sys
import django
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

from django.db import connection

def check_current_state():
    """Проверить текущее состояние базы данных"""
    print("🔍 Проверка текущего состояния...")
    
    with connection.cursor() as cursor:
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"📊 Найдено таблиц: {len(tables)}")
        for table in tables[:10]:  
            print(f"  - {table[0]}")
        
        if len(tables) > 10:
            print(f"  ... и еще {len(tables) - 10} таблиц")
    
    return tables

def fix_migrations():
    """Исправить состояние миграций"""
    print("\n🔧 Исправление состояния миграций...")
    
    with connection.cursor() as cursor:
        
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'django_migrations'
            );
        """)
        exists = cursor.fetchone()[0]
        
        if not exists:
            print("❌ Таблица django_migrations не существует!")
            print("   Запустите: python manage.py migrate")
            return False
        
      
        cursor.execute("DELETE FROM django_migrations;")
        print("✅ Таблица django_migrations очищена")
        
       
        base_migrations = [
            # Системные приложения Django
            ('contenttypes', '0001_initial'),
            ('auth', '0001_initial'),
            ('auth', '0002_alter_permission_name_max_length'),
            ('auth', '0003_alter_user_email_max_length'),
            ('auth', '0004_alter_user_username_opts'),
            ('auth', '0005_alter_user_last_login_null'),
            ('auth', '0006_require_contenttypes_0002'),
            ('auth', '0007_alter_validators_add_error_messages'),
            ('auth', '0008_alter_user_username_max_length'),
            ('auth', '0009_alter_user_last_name_max_length'),
            ('auth', '0010_alter_group_name_max_length'),
            ('auth', '0011_update_proxy_permissions'),
            ('auth', '0012_alter_user_first_name_max_length'),
            
            # Admin
            ('admin', '0001_initial'),
            ('admin', '0002_logentry_remove_auto_add'),
            ('admin', '0003_logentry_add_action_flag_choices'),
            
            # Sessions
            ('sessions', '0001_initial'),
        ]
        
      
        your_apps = [
            'users', 'categories', 'budgets', 'transactions',
            'analytics', 'goals', 'notifications', 'files'
        ]
        
        for app in your_apps:
           
            cursor.execute("""
                SELECT name FROM django_migrations 
                WHERE app = %s 
                ORDER BY name;
            """, [app])
            
            existing = [row[0] for row in cursor.fetchall()]
            
            if not existing:
                
                base_migrations.append((app, '0001_initial'))
                print(f"✅ Добавлена миграция: {app}.0001_initial")
        
        
        for app, name in base_migrations:
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES (%s, %s, NOW());
            """, [app, name])
        
        print(f"✅ Добавлено {len(base_migrations)} записей о миграциях")
        
        return True

def verify_fix():
    """Проверить исправление"""
    print("\n🔍 Проверка исправления...")
    
    with connection.cursor() as cursor:
       
        cursor.execute("""
            SELECT app, name, applied 
            FROM django_migrations 
            ORDER BY app, name;
        """)
        
        migrations = cursor.fetchall()
        
        print(f"📊 Всего записей в django_migrations: {len(migrations)}")
        
       
        apps = {}
        for app, name, applied in migrations:
            if app not in apps:
                apps[app] = []
            apps[app].append(name)
        
        for app in sorted(apps.keys()):
            print(f"  {app}: {len(apps[app])} миграций")
            for migration in apps[app][:3]:  
                print(f"    - {migration}")
            if len(apps[app]) > 3:
                print(f"    ... и еще {len(apps[app]) - 3}")
    
    return True

def create_missing_tables():
    """Создать отсутствующие таблицы"""
    print("\n🛠️  Проверка отсутствующих таблиц...")
    

    expected_tables = [
        'users_user',
        'users_profile',  
        'categories_category',
        'budgets_budget',
        'budgets_budgetmember',
        'transactions_transaction',
        'analytics_report',  
        'goals_goal',  
        'notifications_notification',  
        'files_file'  
    ]
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        existing_tables = {row[0] for row in cursor.fetchall()}
        
        missing_tables = []
        for table in expected_tables:
            if table not in existing_tables:
                missing_tables.append(table)
        
        if missing_tables:
            print(f"⚠️  Отсутствуют таблицы: {len(missing_tables)}")
            for table in missing_tables:
                print(f"  - {table}")
            
            print("\n🔧 Создание отсутствующих таблиц...")
            
          
            for table in missing_tables:
               
                if table.startswith('users_'):
                    print(f"  Применяем миграции для users...")
                    os.system("python manage.py migrate users")
                elif table.startswith('categories_'):
                    print(f"  Применяем миграции для categories...")
                    os.system("python manage.py migrate categories")
                elif table.startswith('budgets_'):
                    print(f"  Применяем миграции для budgets...")
                    os.system("python manage.py migrate budgets")
                elif table.startswith('transactions_'):
                    print(f"  Применяем миграции для transactions...")
                    os.system("python manage.py migrate transactions")
        
        else:
            print("✅ Все ожидаемые таблицы существуют")

def main():
    """Основная функция"""
    print("=" * 70)
    print("🔄 ИСПРАВЛЕНИЕ СОСТОЯНИЯ МИГРАЦИЙ БАЗЫ ДАННЫХ")
    print("=" * 70)
    
    try:
      
        tables = check_current_state()
        
        if not tables:
            print("\n❌ В базе данных нет таблиц!")
            print("   Запустите: python manage.py migrate")
            return
        
        
        if not fix_migrations():
            return
        
        
        create_missing_tables()
        
      
        verify_fix()
        
        print("\n" + "=" * 70)
        print("✅ СОСТОЯНИЕ МИГРАЦИЙ УСПЕШНО ИСПРАВЛЕНО!")
        print("=" * 70)
        print("\n📋 Рекомендуемые действия:")
        print("1. Проверьте миграции: python manage.py showmigrations")
        print("2. Создайте суперпользователя: python manage.py createsuperuser")
        print("3. Запустите сервер: python manage.py runserver")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()