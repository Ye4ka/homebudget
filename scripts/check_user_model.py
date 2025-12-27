#!/usr/bin/env python3
"""
Проверка модели пользователя
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR, os.path.join(BASE_DIR, 'backend')])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

print("🔍 ПРОВЕРКА МОДЕЛИ ПОЛЬЗОВАТЕЛЯ")
print("="*50)

# 1. Проверяем поля модели
print("\n1. Поля модели User:")
for field in User._meta.fields:
    print(f"  {field.name:20} {field.__class__.__name__:15} null={field.null}")

# 2. Проверяем USERNAME_FIELD
print(f"\n2. USERNAME_FIELD: {User.USERNAME_FIELD}")
print(f"   REQUIRED_FIELDS: {User.REQUIRED_FIELDS}")

# 3. Проверяем таблицу в базе
print("\n3. Структура таблицы users_user:")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'users_user'
        ORDER BY ordinal_position;
    """)
    
    for col in cursor.fetchall():
        print(f"  {col[0]:20} {col[1]:20} {'NULL' if col[2]=='YES' else 'NOT NULL':10} {col[3] or ''}")

# 4. Пробуем создать пользователя
print("\n4. Тест создания пользователя:")
try:
    user = User.objects.create_user(
        email='test@test.com',
        password='password123',
        first_name='Test',
        last_name='User'
    )
    print(f"✅ Пользователь создан: {user.email}")
    
    # Проверяем методы
    print(f"   Полное имя: {user.get_full_name()}")
    print(f"   Инициалы: {user.initials}")
    
    # Удаляем тестового пользователя
    user.delete()
    print("✅ Тестовый пользователь удален")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\nВозможные причины:")
    print("1. Модель требует поле username")
    print("2. Неправильные миграции")
    print("3. Смешанные модели (старая и новая)")