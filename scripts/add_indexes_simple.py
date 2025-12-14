#!/usr/bin/env python
"""
ПРОСТОЙ СКРИПТ ДЛЯ ДОБАВЛЕНИЯ ИНДЕКСОВ
Запускать из любой папки
"""
import subprocess
import sys

def run_psql_command(command):
    """Выполнить команду в psql"""
    try:
        # Команда для подключения к PostgreSQL
        cmd = [
            'psql',
            '-U', 'myuser',           # ИЗМЕНИТЕ НА ВАШЕГО ПОЛЬЗОВАТЕЛЯ
            '-d', 'homebudget',       # ИЗМЕНИТЕ ЕСЛИ НУЖНО
            '-h', 'localhost',
            '-p', '5432',
            '-c', command
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_index_exists(table_name, index_name):
    """Проверить существует ли индекс"""
    command = f"""
        SELECT 1 FROM pg_indexes 
        WHERE tablename = '{table_name}' 
        AND indexname = '{index_name}';
    """
    success, output, error = run_psql_command(command)
    return success and "1 row" in output

def create_index(table_name, index_name, index_sql):
    """Создать индекс если он не существует"""
    print(f"🔍 Проверяем индекс {index_name}...")
    
    if check_index_exists(table_name, index_name):
        print(f"✅ {index_name} уже существует")
        return True
    
    print(f"🛠️  Создаем {index_name}...")
    command = f"CREATE INDEX {index_name} {index_sql};"
    success, output, error = run_psql_command(command)
    
    if success:
        print(f"✅ {index_name} успешно создан")
        return True
    else:
        print(f"❌ Ошибка создания {index_name}: {error}")
        return False

def main():
    """Основная функция"""
    print("=" * 70)
    print("🚀 ДОБАВЛЕНИЕ ИНДЕКСОВ В БАЗУ ДАННЫХ HOMEBUDGET")
    print("=" * 70)
    
    # Индексы для добавления
    indexes = [
        # Таблица: notifications_notification
        {
            'table': 'notifications_notification',
            'name': 'idx_user_read',
            'sql': 'ON notifications_notification(user_id, is_read)'
        },
        {
            'table': 'notifications_notification',
            'name': 'idx_created_at_desc',
            'sql': 'ON notifications_notification(created_at DESC)'
        },
        
        # Таблица: transactions_transaction
        {
            'table': 'transactions_transaction',
            'name': 'idx_budget_date',
            'sql': 'ON transactions_transaction(budget_id, date DESC)'
        },
        {
            'table': 'transactions_transaction',
            'name': 'idx_budget_category',
            'sql': 'ON transactions_transaction(budget_id, category_id)'
        },
        {
            'table': 'transactions_transaction',
            'name': 'idx_trans_type',
            'sql': 'ON transactions_transaction(type)'
        },
        {
            'table': 'transactions_transaction',
            'name': 'idx_budget_type',
            'sql': 'ON transactions_transaction(budget_id, type)'
        },
    ]
    
    created_count = 0
    existing_count = 0
    error_count = 0
    
    for idx in indexes:
        if create_index(idx['table'], idx['name'], idx['sql']):
            created_count += 1
        else:
            error_count += 1
    
    # Проверка всех индексов
    print("\n" + "=" * 70)
    print("📊 ПРОВЕРКА ВСЕХ ИНДЕКСОВ")
    print("=" * 70)
    
    success, output, error = run_psql_command("""
        SELECT 
            tablename,
            indexname,
            pg_size_pretty(pg_relation_size(schemaname||'.'||indexname)) as size
        FROM pg_indexes 
        WHERE schemaname = 'public'
        AND tablename IN ('notifications_notification', 'transactions_transaction')
        ORDER BY tablename, indexname;
    """)
    
    if success:
        print("📈 Список индексов:")
        print(output)
    else:
        print(f"❌ Ошибка получения списка индексов: {error}")
    
    # Итог
    print("\n" + "=" * 70)
    print("🎯 ИТОГ")
    print("=" * 70)
    print(f"✅ Создано новых индексов: {created_count}")
    print(f"📊 Уже существовало: {existing_count}")
    print(f"❌ Ошибок: {error_count}")
    
    if error_count == 0:
        print("\n🎉 ЗАДАЧА 3: ИНДЕКСЫ УСПЕШНО ДОБАВЛЕНЫ!")
        print("\n📋 Что дальше:")
        print("1. Создайте ER-диаграмму на dbdiagram.io")
        print("2. Создайте docs/database/indexes-documentation.md")
        print("3. Создайте docs/database/database-schema.md")
    else:
        print("\n⚠️  Были ошибки. Проверьте подключение к БД.")

if __name__ == "__main__":
    main()