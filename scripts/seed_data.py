#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Добавляем корень проекта в путь
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except django.core.exceptions.ImproperlyConfigured as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

# Пробуем разные варианты импорта
try:
    # Вариант 1: apps. префикс
    from apps.users.models import User
    from apps.budgets.models import Budget, BudgetMember
    from apps.categories.models import Category
    from apps.transactions.models import Transaction
    print("✅ Импорт через apps. префикс")
except ImportError:
    try:
        # Вариант 2: Без префикса
        from users.models import User
        from budgets.models import Budget, BudgetMember
        from categories.models import Category
        from transactions.models import Transaction
        print("✅ Импорт без префикса")
    except ImportError as e:
        print(f"❌ Не удалось импортировать модели: {e}")
        print("\nПроверь структуру папок:")
        print(f"Текущая папка: {os.getcwd()}")
        print(f"Содержимое apps/:")
        apps_path = os.path.join(BASE_DIR, 'apps')
        if os.path.exists(apps_path):
            for item in os.listdir(apps_path):
                print(f"  - {item}")
        sys.exit(1)

def create_users():
    """Создаем 3 тестовых пользователя"""
    users = []
    
    users_data = [
        {'username': 'alex', 'email': 'alex@example.com', 'currency': 'RUB'},
        {'username': 'maria', 'email': 'maria@example.com', 'currency': 'USD'},
        {'username': 'ivan', 'email': 'ivan@example.com', 'currency': 'EUR'},
    ]
    
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'currency': data['currency']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✅ Создан пользователь: {user.username}")
        else:
            print(f"⚠️  Пользователь {user.username} уже существует")
        users.append(user)
    
    return users

def create_budgets(users):
    """Создаем 2 бюджета"""
    budgets = []
    
    # Личный бюджет
    personal_budget, created = Budget.objects.get_or_create(
        name='Личный бюджет Алекса',
        defaults={
            'type': 'personal',
            'owner': users[0],
            'currency': users[0].currency
        }
    )
    if created:
        budgets.append(personal_budget)
        print(f"✅ Создан личный бюджет: {personal_budget.name}")
    
    # Семейный бюджет
    family_budget, created = Budget.objects.get_or_create(
        name='Семейный бюджет',
        defaults={
            'type': 'family', 
            'owner': users[0],
            'currency': 'RUB'
        }
    )
    if created:
        budgets.append(family_budget)
        print(f"✅ Создан семейный бюджет: {family_budget.name}")
        
        # Добавляем участников
        for i, user in enumerate(users[1:], 1):
            BudgetMember.objects.get_or_create(
                budget=family_budget,
                user=user,
                defaults={'role': 'editor' if i == 1 else 'viewer'}
            )
            print(f"✅ Добавлен участник {user.username} в семейный бюджет")
    
    return budgets

def create_transactions(budgets, users):
    """Создаем 50 тестовых транзакций"""
    categories = Category.objects.filter(is_default=True)
    today = datetime.now().date()
    
    if not categories.exists():
        print("❌ Нет категорий! Сначала загрузи fixtures/categories.json")
        return
    
    transaction_count = 0
    
    for i in range(50):
        # Случайный бюджет
        budget = random.choice(budgets)
        
        # 70% расходы, 30% доходы
        if random.random() < 0.7:
            trans_type = 'expense'
            amount = round(random.uniform(100, 5000), 2)
            expense_categories = categories.filter(type='expense')
            if not expense_categories.exists():
                continue
            category = random.choice(expense_categories)
        else:
            trans_type = 'income'
            amount = round(random.uniform(1000, 20000), 2)
            income_categories = categories.filter(type='income')
            if not income_categories.exists():
                continue
            category = random.choice(income_categories)
        
        # Случайная дата (последние 90 дней)
        days_ago = random.randint(0, 90)
        trans_date = today - timedelta(days=days_ago)
        
        # Случайный пользователь-создатель
        if budget.type == 'personal':
            created_by = budget.owner
        else:
            members = list(BudgetMember.objects.filter(budget=budget))
            created_by = random.choice([m.user for m in members]) if members else budget.owner
        
        # Создаем транзакцию
        Transaction.objects.create(
            amount=amount,
            type=trans_type,
            description=f'Тестовая транзакция #{i+1}',
            date=trans_date,
            category=category,
            budget=budget,
            created_by=created_by
        )
        transaction_count += 1
    
    print(f"✅ Создано {transaction_count} транзакций")

def main():
    print("🚀 Начало создания тестовых данных...")
    print("=" * 50)
    
    # 1. Пользователи
    users = create_users()
    
    # 2. Бюджеты
    budgets = create_budgets(users)
    
    # 3. Транзакции
    create_transactions(budgets, users)
    
    # 4. Статистика
    print("=" * 50)
    print("📊 Статистика:")
    print(f"👤 Пользователей: {User.objects.count()}")
    print(f"💰 Бюджетов: {Budget.objects.count()}")
    print(f"📊 Транзакций: {Transaction.objects.count()}")
    print(f"🏷️  Категорий: {Category.objects.count()}")
    print("🎉 Готово!")

if __name__ == "__main__":
    main()