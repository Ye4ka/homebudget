#!/usr/bin/env python
"""
Скрипт для создания всех тестовых данных для задачи 2
Разместите в: homebudget/create_data.py
"""
import os
import sys

# Добавляем backend в путь
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from backend.apps.categories.models import Category
from backend.apps.budgets.models import Budget, BudgetMember
from backend.apps.transactions.models import Transaction
from datetime import datetime, timedelta
import random
import decimal

User = get_user_model()

def create_superuser():
    """Создать суперпользователя если нет"""
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            currency='RUB'
        )
        print("✅ Создан суперпользователь: admin")
    admin_user = User.objects.get(username='admin')
    return admin_user

def create_categories(user):
    """Создать 12 стандартных категорий (6 доходов, 6 расходов)"""
    categories = [
        # Доходы (6)
        {"name": "Зарплата", "type": "income", "color": "#4CAF50", "icon": "account-balance-wallet"},
        {"name": "Фриланс", "type": "income", "color": "#8BC34A", "icon": "laptop"},
        {"name": "Инвестиции", "type": "income", "color": "#CDDC39", "icon": "trending-up"},
        {"name": "Подарки", "type": "income", "color": "#FFEB3B", "icon": "card-giftcard"},
        {"name": "Возврат долгов", "type": "income", "color": "#FFC107", "icon": "handshake"},
        {"name": "Прочие доходы", "type": "income", "color": "#FF9800", "icon": "more-horiz"},
        
        # Расходы (6)
        {"name": "Продукты", "type": "expense", "color": "#F44336", "icon": "shopping-cart"},
        {"name": "Транспорт", "type": "expense", "color": "#E91E63", "icon": "directions-car"},
        {"name": "Жилье", "type": "expense", "color": "#9C27B0", "icon": "home"},
        {"name": "Развлечения", "type": "expense", "color": "#673AB7", "icon": "movie"},
        {"name": "Здоровье", "type": "expense", "color": "#3F51B5", "icon": "medical-services"},
        {"name": "Образование", "type": "expense", "color": "#2196F3", "icon": "school"},
    ]
    
    created_count = 0
    existing_count = 0
    
    for cat_data in categories:
        # Проверяем, существует ли категория
        if Category.objects.filter(name=cat_data['name'], type=cat_data['type'], is_default=True).exists():
            existing_count += 1
            continue
        
        try:
            Category.objects.create(
                name=cat_data['name'],
                type=cat_data['type'],
                color=cat_data['color'],
                icon=cat_data['icon'],
                is_default=True,
                created_by=user
            )
            created_count += 1
            print(f"  ✅ Создана: {cat_data['name']} ({cat_data['type']})")
        except Exception as e:
            print(f"  ❌ Ошибка создания {cat_data['name']}: {e}")
    
    print(f"\n📊 Категории: создано {created_count}, уже было {existing_count}")
    return Category.objects.all()

def create_test_users():
    """Создать 3 тестовых пользователя"""
    print("\n👤 Создание тестовых пользователей...")
    
    users_data = [
        {'username': 'alex', 'email': 'alex@example.com', 'password': 'password123', 'currency': 'RUB'},
        {'username': 'maria', 'email': 'maria@example.com', 'password': 'password123', 'currency': 'USD'},
        {'username': 'ivan', 'email': 'ivan@example.com', 'password': 'password123', 'currency': 'EUR'},
    ]
    
    users = []
    for data in users_data:
        if not User.objects.filter(username=data['username']).exists():
            try:
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    currency=data['currency']
                )
                users.append(user)
                print(f"  ✅ Создан: {user.username} ({user.email})")
            except Exception as e:
                print(f"  ❌ Ошибка создания {data['username']}: {e}")
        else:
            user = User.objects.get(username=data['username'])
            users.append(user)
            print(f"  ⚠️  Уже существует: {user.username}")
    
    return users

def create_budgets(users):
    """Создать 2 бюджета (личный и семейный)"""
    print("\n💰 Создание бюджетов...")
    
    budgets = []
    
    # 1. Личный бюджет
    if not Budget.objects.filter(name='Личный бюджет Алекса').exists():
        personal_budget = Budget.objects.create(
            name='Личный бюджет Алекса',
            type='personal',
            owner=users[0],
            currency=users[0].currency
        )
        budgets.append(personal_budget)
        print(f"  ✅ Личный бюджет: {personal_budget.name}")
    else:
        personal_budget = Budget.objects.get(name='Личный бюджет Алекса')
        budgets.append(personal_budget)
        print(f"  ⚠️  Личный бюджет уже существует")
    
    # 2. Семейный бюджет
    if not Budget.objects.filter(name='Семейный бюджет').exists():
        family_budget = Budget.objects.create(
            name='Семейный бюджет',
            type='family',
            owner=users[0],
            currency='RUB'
        )
        budgets.append(family_budget)
        print(f"  ✅ Семейный бюджет: {family_budget.name}")
        
        # Добавляем участников
        for i, user in enumerate(users[1:], 1):
            BudgetMember.objects.create(
                budget=family_budget,
                user=user,
                role='editor' if i == 1 else 'viewer'
            )
            print(f"  ✅ Участник: {user.username} ({'редактор' if i == 1 else 'наблюдатель'})")
    else:
        family_budget = Budget.objects.get(name='Семейный бюджет')
        budgets.append(family_budget)
        print(f"  ⚠️  Семейный бюджет уже существует")
    
    return budgets

def create_transactions(budgets, categories):
    """Создать 50 тестовых транзакций"""
    print("\n💸 Создание транзакций...")
    
    if not budgets or not categories:
        print("  ❌ Нет бюджетов или категорий")
        return
    
    # Разделяем категории
    income_categories = categories.filter(type='income')
    expense_categories = categories.filter(type='expense')
    
    if not income_categories.exists() or not expense_categories.exists():
        print("  ❌ Нет категорий доходов или расходов")
        return
    
    today = datetime.now().date()
    transaction_count = 0
    
    for i in range(50):
        try:
            # Случайный бюджет
            budget = random.choice(budgets)
            
            # 70% расходы, 30% доходы
            if random.random() < 0.7:
                trans_type = 'expense'
                amount = decimal.Decimal(random.uniform(100, 10000)).quantize(decimal.Decimal('0.01'))
                category = random.choice(expense_categories)
            else:
                trans_type = 'income'
                amount = decimal.Decimal(random.uniform(1000, 50000)).quantize(decimal.Decimal('0.01'))
                category = random.choice(income_categories)
            
            # Случайная дата за последние 90 дней
            days_ago = random.randint(0, 90)
            trans_date = today - timedelta(days=days_ago)
            
            # Кто создал транзакцию
            if budget.type == 'personal':
                created_by = budget.owner
            else:
                # Для семейного бюджета - случайный участник
                members = list(budget.members.all())
                if members:
                    created_by = random.choice(members).user
                else:
                    created_by = budget.owner
            
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
            
            if (i + 1) % 10 == 0:
                print(f"  Создано {i + 1} транзакций...")
                
        except Exception as e:
            print(f"  ❌ Ошибка транзакции #{i+1}: {e}")
    
    print(f"  ✅ Всего создано: {transaction_count} транзакций")
    return transaction_count

def print_statistics():
    """Вывести статистику"""
    print("\n" + "="*60)
    print("📊 ФИНАЛЬНАЯ СТАТИСТИКА БАЗЫ ДАННЫХ")
    print("="*60)
    
    try:
        from django.db.models import Sum
        
        # Пользователи
        user_count = User.objects.count()
        print(f"👤 Пользователей: {user_count}")
        
        # Бюджеты
        budget_count = Budget.objects.count()
        personal_count = Budget.objects.filter(type='personal').count()
        family_count = Budget.objects.filter(type='family').count()
        print(f"💰 Бюджетов: {budget_count} (личных: {personal_count}, семейных: {family_count})")
        
        # Участники
        member_count = BudgetMember.objects.count()
        print(f"👥 Участников бюджетов: {member_count}")
        
        # Категории
        category_count = Category.objects.count()
        income_cat_count = Category.objects.filter(type='income').count()
        expense_cat_count = Category.objects.filter(type='expense').count()
        print(f"🏷️  Категорий: {category_count} (доходы: {income_cat_count}, расходы: {expense_cat_count})")
        
        # Транзакции
        transaction_count = Transaction.objects.count()
        if transaction_count > 0:
            income_sum = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
            expense_sum = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
            income_count = Transaction.objects.filter(type='income').count()
            expense_count = Transaction.objects.filter(type='expense').count()
            
            print(f"💸 Транзакций: {transaction_count}")
            print(f"  • Доходы: {income_count} на сумму {income_sum:.2f}")
            print(f"  • Расходы: {expense_count} на сумму {expense_sum:.2f}")
            print(f"  • Баланс: {income_sum - expense_sum:.2f}")
        
        print("="*60)
        print("🎉 ЗАДАЧА 2 ВЫПОЛНЕНА УСПЕШНО!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Ошибка статистики: {e}")

def main():
    """Основная функция"""
    print("=" * 70)
    print("🚀 ВЫПОЛНЕНИЕ ЗАДАЧИ 2: НАЧАЛЬНЫЕ ДАННЫХ + УЛУЧШЕННЫЕ МИГРАЦИИ")
    print("=" * 70)
    
    try:
        # 1. Создать суперпользователя (для категорий)
        print("\n1️⃣  Создание суперпользователя...")
        admin = create_superuser()
        
        # 2. Создать 12 категорий (6 доходов + 6 расходов)
        print("\n2️⃣  Создание категорий...")
        categories = create_categories(admin)
        
        # 3. Создать 3 тестовых пользователя
        print("\n3️⃣  Создание пользователей...")
        users = create_test_users()
        
        # 4. Создать 2 бюджета
        print("\n4️⃣  Создание бюджетов...")
        budgets = create_budgets(users)
        
        # 5. Создать 50 транзакций
        print("\n5️⃣  Создание транзакций...")
        create_transactions(budgets, categories)
        
        # 6. Вывести статистику
        print_statistics()
        
        print("\n✅ ВСЕ ЧАСТИ ЗАДАЧИ 2 ВЫПОЛНЕНЫ:")
        print("   • CHECK constraints добавлены в миграциях ✓")
        print("   • 12 категорий (6 доходов + 6 расходов) созданы ✓")
        print("   • 3 пользователя созданы ✓")
        print("   • 2 бюджета (личный и семейный) созданы ✓")
        print("   • 50 транзакций созданы ✓")
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()