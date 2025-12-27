#!/usr/bin/env python3
"""
Исправленный скрипт заполнения данных
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR, os.path.join(BASE_DIR, 'backend')])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from apps.budgets.models import Budget
from apps.categories.models import Category
from apps.transactions.models import Transaction
from decimal import Decimal
from datetime import date, timedelta
import random

User = get_user_model()

def check_user_model():
    """Проверить модель пользователя."""
    print("🔍 Проверка модели User...")
    
    # Проверяем нужные поля
    required_fields = ['email', 'first_name', 'last_name']
    for field_name in required_fields:
        try:
            field = User._meta.get_field(field_name)
            print(f" Поле {field_name}: найдено")
        except:
            print(f" Поле {field_name}: не найдено")
            return False
    
    # Проверяем USERNAME_FIELD
    if User.USERNAME_FIELD != 'email':
        print(f"⚠️  USERNAME_FIELD = {User.USERNAME_FIELD}, ожидалось 'email'")
        # Все равно продолжаем, но предупреждаем
    
    return True

def create_users_safe():
    """Безопасное создание пользователей."""
    print("\n👥 Создание пользователей...")
    
    users_data = [
        {'email': 'alex@homebudget.com', 'password': 'password123', 
         'first_name': 'Алексей', 'last_name': 'Иванов'},
        {'email': 'maria@homebudget.com', 'password': 'password123', 
         'first_name': 'Мария', 'last_name': 'Петрова'},
        {'email': 'dmitry@homebudget.com', 'password': 'password123', 
         'first_name': 'Дмитрий', 'last_name': 'Сидоров'},
    ]
    
    users = []
    
    for data in users_data:
        try:
            # Пробуем разные варианты создания
            if hasattr(User.objects, 'create_user'):
                # Новая модель с UserManager
                user = User.objects.create_user(**data)
            else:
                # Старая модель
                user = User.objects.create(
                    username=data['email'],  # Для старых моделей
                    email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )
                user.set_password(data['password'])
                user.save()
            
            print(f" Создан: {user.email}")
            users.append(user)
            
        except Exception as e:
            print(f" Ошибка создания {data['email']}: {e}")
            print("   Пробуем альтернативный метод...")
            
            try:
                # Альтернативный способ через raw SQL
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO users_user 
                        (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO NOTHING
                    """, [
                        'pbkdf2_sha256$260000$...',  # Заглушка, на практике нужно хэшировать
                        False,
                        data['email'],
                        data['first_name'],
                        data['last_name'],
                        data['email'],
                        False,
                        True,
                        'now()'
                    ])
                
                user = User.objects.get(email=data['email'])
                user.set_password(data['password'])
                user.save()
                
                print(f" Создан через SQL: {user.email}")
                users.append(user)
                
            except Exception as e2:
                print(f" Полная ошибка: {e2}")
    
    return users

def create_users_simple():
    """Простое создание пользователей (если другие методы не работают)."""
    print("\n👥 Простое создание пользователей...")
    
    users = []
    emails = ['alex@homebudget.com', 'maria@homebudget.com', 'dmitry@homebudget.com']
    
    for email in emails:
        # Проверяем существование
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print(f" Уже существует: {user.email}")
        else:
            try:
                # Простой способ
                user = User(
                    email=email,
                    first_name='Тест',
                    last_name='Пользователь',
                    is_active=True
                )
                user.set_password('password123')
                user.save()
                print(f" Создан: {user.email}")
            except Exception as e:
                print(f" Ошибка: {e}")
                # Создаем через admin если ничего не помогает
                continue
        
        users.append(user)
    
    return users

def ensure_categories():
    """Создать категории."""
    print("\n  Создание категорий...")
    
    categories = [
        # Доходы
        ('Зарплата', 'income', '#10B981', 'Cash'),
        ('Фриланс', 'income', '#3B82F6', 'Code'),
        ('Инвестиции', 'income', '#8B5CF6', 'TrendingUp'),
        ('Подарки', 'income', '#EC4899', 'Gift'),
        ('Возврат долга', 'income', '#14B8A6', 'HandCoins'),
        ('Прочие доходы', 'income', '#6366F1', 'MoreHorizontal'),
        
        # Расходы
        ('Продукты', 'expense', '#EF4444', 'ShoppingCart'),
        ('Транспорт', 'expense', '#F59E0B', 'Car'),
        ('Жилье', 'expense', '#84CC16', 'Home'),
        ('Развлечения', 'expense', '#06B6D4', 'Gamepad2'),
        ('Одежда', 'expense', '#8B5CF6', 'Shirt'),
        ('Прочие расходы', 'expense', '#71717A', 'MoreHorizontal'),
    ]
    
    created = 0
    for name, type_, color, icon in categories:
        if not Category.objects.filter(name=name, type=type_).exists():
            try:
                Category.objects.create(
                    name=name,
                    type=type_,
                    color=color,
                    icon=icon,
                    is_system=True
                )
                created += 1
                print(f" Создана: {name}")
            except Exception as e:
                print(f" Ошибка {name}: {e}")
    
    print(f"Всего категорий: {Category.objects.count()} (+{created} новых)")
    
    return (
        list(Category.objects.filter(type='income')),
        list(Category.objects.filter(type='expense'))
    )

def create_budgets_for_users(users):
    """Создать бюджеты для пользователей."""
    print("\n💰 Создание бюджетов...")
    
    budgets = []
    
    for user in users:
        # Личный бюджет
        try:
            budget_name = f"Бюджет {user.first_name}"
            budget, created = Budget.objects.get_or_create(
                name=budget_name,
                owner=user,
                defaults={
                    'type': Budget.TYPE_PERSONAL,
                    'currency': Budget.CURRENCY_RUB
                }
            )
            
            if created:
                print(f" Личный бюджет: {budget.name}")
            budgets.append(budget)
        except Exception as e:
            print(f" Ошибка бюджета для {user.email}: {e}")
    
    # Семейный бюджет
    if users:
        try:
            family_budget, created = Budget.objects.get_or_create(
                name="Семейный бюджет",
                owner=users[0],
                type=Budget.TYPE_FAMILY,
                defaults={'currency': Budget.CURRENCY_USD}
            )
            
            if created:
                print(f" Семейный бюджет: {family_budget.name}")
            budgets.append(family_budget)
        except Exception as e:
            print(f" Ошибка семейного бюджета: {e}")
    
    return budgets

def add_sample_transactions(budgets, income_cats, expense_cats):
    """Добавить примерные транзакции."""
    print("\n Добавление транзакций...")
    
    today = date.today()
    total_added = 0
    
    for budget in budgets:
        # Пропускаем если уже много транзакций
        existing = Transaction.objects.filter(budget=budget).count()
        if existing > 5:
            print(f"⏭  У {budget.name} уже {existing} транзакций")
            continue
        
        print(f" Бюджет: {budget.name}")
        added = 0
        
        # 10 транзакций на бюджет
        for i in range(10):
            is_income = random.choice([True, False])
            category = random.choice(income_cats if is_income else expense_cats)
            
            # Сумма в зависимости от категории
            if category.name == 'Зарплата':
                amount = Decimal('75000.00')
            elif category.name == 'Жилье':
                amount = Decimal('25000.00')
            elif category.name == 'Продукты':
                amount = Decimal('5000.00')
            else:
                amount = Decimal(str(round(random.uniform(100, 10000), 2)))
            
            # Дата - случайная за последние 30 дней
            days_ago = random.randint(0, 30)
            trans_date = today - timedelta(days=days_ago)
            
            try:
                Transaction.objects.create(
                    budget=budget,
                    category=category,
                    type='income' if is_income else 'expense',
                    amount=amount,
                    description=f"{category.name} #{i+1}",
                    date=trans_date,
                    created_by=budget.owner
                )
                added += 1
                total_added += 1
            except Exception as e:
                print(f"     Ошибка транзакции: {e}")
        
        if added > 0:
            print(f"    Добавлено: {added} транзакций")
    
    return total_added

def main():
    """Основная функция."""
    print("="*60)
    print(" ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ")
    print("="*60)
    
    # 1. Проверяем модель
    if not check_user_model():
        print("\n Проблема с моделью User!")
        print("Проверьте миграции или запустите:")
        print("python manage.py makemigrations users")
        print("python manage.py migrate users")
        return
    
    # 2. Создаем пользователей
    users = create_users_simple()
    if not users:
        print("\n Не удалось создать пользователей")
        print("Создайте хотя бы одного вручную:")
        print("python manage.py createsuperuser")
        return
    
    # 3. Создаем категории
    income_cats, expense_cats = ensure_categories()
    if not income_cats or not expense_cats:
        print(" Нет категорий")
        return
    
    # 4. Создаем бюджеты
    budgets = create_budgets_for_users(users)
    if not budgets:
        print("Нет бюджетов")
        return
    
    # 5. Добавляем транзакции
    print("\n⏳ Добавление транзакций...")
    transactions_added = add_sample_transactions(budgets, income_cats, expense_cats)
    
    # 6. Результат
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТ:")
    print(f"   Пользователей: {User.objects.count()}")
    print(f"   Бюджетов: {Budget.objects.count()}")
    print(f"   Категорий: {Category.objects.count()}")
    print(f"   Транзакций: {Transaction.objects.count()}")
    print(f"   (+{transactions_added} новых)")
    
    # Пример работы
    if Budget.objects.exists():
        budget = Budget.objects.first()
        print(f"\n💎 Пример - бюджет '{budget.name}':")
        print(f"   Баланс: {budget.get_balance()} {budget.currency}")
        print(f"   Транзакций: {budget.transactions.count()}")
    
    print("\nГОТОВО!")

if __name__ == '__main__':
    main()