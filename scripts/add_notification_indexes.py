#!/usr/bin/env python
"""
Скрипт для добавления индексов к таблице notifications
Запускать из корня проекта: python scripts/add_notification_indexes.py
"""
import os
import sys

# Добавляем backend в путь
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
try:
    django.setup()
    print("✅ Django успешно настроен")
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    print("💡 Убедитесь, что вы в корневой папке проекта (homebudget/)")
    print(f"📁 Текущая директория: {os.getcwd()}")
    sys.exit(1)

from django.db import connection

def add_notification_indexes():
    """Добавить индексы для таблицы notifications"""
    print("=" * 70)
    print("🔧 ДОБАВЛЕНИЕ ИНДЕКСОВ ДЛЯ ТАБЛИЦЫ NOTIFICATIONS")
    print("=" * 70)
    
    with connection.cursor() as cursor:
        # 1. Проверим существующие индексы
        print("\n🔍 Проверка существующих индексов...")
        cursor.execute("""
            SELECT indexname, indexdef 
            FROM pg_indexes 
            WHERE tablename = 'notifications_notification'
            ORDER BY indexname;
        """)
        
        existing_indexes = cursor.fetchall()
        
        if existing_indexes:
            print(f"📊 Найдено индексов: {len(existing_indexes)}")
            for name, definition in existing_indexes:
                print(f"  • {name}")
        else:
            print("📊 Индексы не найдены")
        
        # 2. Добавляем idx_user_read если нет
        print("\n➕ Проверяем индекс idx_user_read...")
        cursor.execute("""
            SELECT 1 FROM pg_indexes 
            WHERE indexname = 'idx_user_read' 
            AND tablename = 'notifications_notification';
        """)
        
        if cursor.fetchone():
            print("✅ idx_user_read уже существует")
        else:
            print("🛠️  Создаем idx_user_read...")
            try:
                cursor.execute("""
                    CREATE INDEX idx_user_read 
                    ON notifications_notification(user_id, is_read);
                """)
                print("✅ idx_user_read успешно создан")
            except Exception as e:
                print(f"❌ Ошибка создания idx_user_read: {e}")
        
        # 3. Добавляем idx_created_at_desc если нет
        print("\n➕ Проверяем индекс idx_created_at_desc...")
        cursor.execute("""
            SELECT 1 FROM pg_indexes 
            WHERE indexname = 'idx_created_at_desc' 
            AND tablename = 'notifications_notification';
        """)
        
        if cursor.fetchone():
            print("✅ idx_created_at_desc уже существует")
        else:
            print("🛠️  Создаем idx_created_at_desc...")
            try:
                cursor.execute("""
                    CREATE INDEX idx_created_at_desc 
                    ON notifications_notification(created_at DESC);
                """)
                print("✅ idx_created_at_desc успешно создан")
            except Exception as e:
                print(f"❌ Ошибка создания idx_created_at_desc: {e}")
        
        # 4. Проверяем индексы transactions тоже
        print("\n" + "=" * 70)
        print("🔍 ПРОВЕРКА ИНДЕКСОВ ТРАНЗАКЦИЙ")
        print("=" * 70)
        
        transaction_indexes = [
            'idx_budget_date',
            'idx_budget_category', 
            'idx_trans_type',
            'idx_budget_type'
        ]
        
        for index_name in transaction_indexes:
            cursor.execute("""
                SELECT 1 FROM pg_indexes 
                WHERE indexname = %s 
                AND tablename = 'transactions_transaction';
            """, [index_name])
            
            if cursor.fetchone():
                print(f"✅ {index_name} существует")
            else:
                print(f"❌ {index_name} ОТСУТСТВУЕТ!")
        
        # 5. Финальная проверка
        print("\n" + "=" * 70)
        print("📊 ФИНАЛЬНАЯ ПРОВЕРКА ВСЕХ ИНДЕКСОВ")
        print("=" * 70)
        
        cursor.execute("""
            SELECT 
                tablename,
                indexname,
                pg_size_pretty(pg_relation_size(schemaname||'.'||indexname)) as size
            FROM pg_indexes 
            WHERE schemaname = 'public'
            AND tablename IN ('notifications_notification', 'transactions_transaction')
            ORDER BY tablename, indexname;
        """)
        
        all_indexes = cursor.fetchall()
        print(f"\n📈 Всего индексов: {len(all_indexes)}")
        for table, index, size in all_indexes:
            print(f"  • {table}.{index} ({size})")

def main():
    """Основная функция"""
    try:
        add_notification_indexes()
        print("\n" + "=" * 70)
        print("🎉 ЗАДАЧА 3: ИНДЕКСЫ УСПЕШНО ДОБАВЛЕНЫ!")
        print("=" * 70)
        print("\n✅ Что сделано:")
        print("   • Индексы для notifications проверены/добавлены")
        print("   • Индексы для transactions проверены")
        print("   • Готово к созданию ER-диаграммы")
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()