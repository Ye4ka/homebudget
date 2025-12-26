import psycopg2

try:
    conn = psycopg2.connect(
        dbname='homebudget',
        user='myuser',
        password='mypassword',
        host='localhost',
        port='5432'
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    print(f"Успешно PostgreSQL: {cursor.fetchone()[0].split(',')[0]}")
    
    cursor.execute("SELECT current_database();")
    print(f"Успешно База данных: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
    table_count = cursor.fetchone()[0]
    print(f"Успешно. Таблиц в БД: {table_count}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Ошибка: {e}")