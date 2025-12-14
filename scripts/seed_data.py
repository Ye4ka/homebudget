#!/usr/bin/env python
import os
import sys
import django
import random
import decimal
from datetime import datetime, timedelta

# Настройка Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

# Импорт моделей
try:
    from backend.apps.users.models import User
    from backend.apps.budgets.models import Budget, BudgetMember
    from backend.apps.categories.models import Category
    from backend.apps.transactions.models import Transaction
    print("✅ Модели успешно импортированы")
except ImportError as e:
    print(f"❌ Ошибка импорта моделей: {e}")
    sys.exit(1)

def create_users():
    """Создаем тестовых пользователей"""
    print("👤 Создание пользователей...")
    users = []
    
    users_data = [
        {'username': 'alex', 'email': 'alex@example.com', 'password': 'password123', 'currency': 'RUB'},
        {'username': 'maria', 'email': 'maria@example.com', 'password': 'password123', 'currency': 'USD'},
        {'username': 'ivan', 'email': 'ivan@example.com', 'password': 'password123', 'currency': 'EUR'},
    ]
    
    for data in users_data:
        # Проверяем, существует ли пользователь
        if User.objects.filter(username=data['username']).exists():
            user = User.objects.get(username=data['username'])
            print(f"⚠️  Пользователь {user.username} уже существует")
        else:
            try:
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    currency=data['currency']
                )
                print(f"✅ Создан пользователь: {user.username}")
            except Exception as e:
                print(f"❌ Ошибка создания пользователя {data['username']}: {e}")
                continue
        
        users.append(user)
    
    return users

def create_budgets(users):
    """Создаем бюджеты"""
    print("\n💰 Создание бюджетов...")
    budgets = []
    
    if not users:
        print("❌ Нет пользователей для создания бюджетов")
        return budgets
    
    # Личный бюджет
    if not Budget.objects.filter(name='Личный бюджет Алекса').exists():
        personal_budget = Budget.objects.create(
            name='Личный бюджет Алекса',
            type='personal',
            owner=users[0],
            currency=users[0].currency
        )
        budgets.append(personal_budget)
        print(f"✅ Создан личный бюджет: {personal_budget.name}")
    else:
        personal_budget = Budget.objects.get(name='Личный бюджет Алекса')
        budgets.append(personal_budget)
        print(f"⚠️  Личный бюджет уже существует: {personal_budget.name}")
    
    # Семейный бюджет
    if not Budget.objects.filter(name='Семейный бюджет').exists():
        family_budget = Budget.objects.create(
            name='Семейный бюджет',
            type='family',
            owner=users[0],
            currency='RUB'
        )
        budgets.append(family_budget)
        print(f"✅ Создан семейный бюджет: {family_budget.name}")
        
        # Добавляем участников
        for user in users[1:]:
            if not BudgetMember.objects.filter(budget=family_budget, user=user).exists():
                BudgetMember.objects.create(
                    budget=family_budget,
                    user=user,
                    role='editor' if user.username == 'maria' else 'viewer'
                )
                print(f"✅ Добавлен участник {user.username} в семейный бюджет")
    else:
        family_budget = Budget.objects.get(name='Семейный бюджет')
        budgets.append(family_budget)
        print(f"⚠️  Семейный бюджет уже существует: {family_budget.name}")
    
    return budgets

def create_transactions(budgets, users):
    """Создаем транзакции"""
    print("\n💸 Создание транзакций...")
    
    if not budgets:
        print("❌ Нет бюджетов для создания транзакций")
        return
    
    # Проверяем категории
    categories = Category.objects.all()
    if not categories.exists():
        print("❌ Нет категорий! Сначала выполните: python manage.py loaddata categories.json")
        return
    
    income_categories = categories.filter(type='income')
    expense_categories = categories.filter(type='expense')
    
    if not income_categories.exists() or not expense_categories.exists():
        print("❌ Не хватает категорий доходов или расходов")
        return
    
    today = datetime.now().date()
    transaction_count = 0
    
    for i in range(50):
        try:
            # Выбираем случайный бюджет
            budget = random.choice(budgets)
            
            # 70% расходы, 30% доходы
            if random.random() < 0.7:
                trans_type = 'expense'
                amount = decimal.Decimal(random.uniform(100, 5000)).quantize(decimal.Decimal('0.01'))
                category = random.choice(expense_categories)
            else:
                trans_type = 'income'
                amount = decimal.Decimal(random.uniform(1000, 20000)).quantize(decimal.Decimal('0.01'))
                category = random.choice(income_categories)
            
            # Случайная дата за последние 90 дней
            days_ago = random.randint(0, 90)
            trans_date = today - timedelta(days=days_ago)
            
            # Выбираем кто создал транзакцию
            if budget.type == 'personal':
                created_by = budget.owner
            else:
                # Для семейного бюджета берем случайного участника
                members = list(budget.members.all())
                if members:
                    created_by = random.choice(members).user
                else:
                    created_by = budget.owner
            
            # Создаем транзакцию
            Transaction.objects.create(
                amount=amount,
                type=trans_type,
                description=f'Тестовая транзакция #{i+1} ({trans_type})',
                date=trans_date,
                category=category,
                budget=budget,
                created_by=created_by
            )
            
            transaction_count += 1
            
            if (i + 1) % 10 == 0:
                print(f"  Создано {i + 1} транзакций...")
                
        except Exception as e:
            print(f"❌ Ошибка создания транзакции #{i+1}: {e}")
    
    print(f"✅ Всего создано {transaction_count} транзакций")

def print_statistics():
    """Вывод статистики"""
    print("\n" + "="*50)
    print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
    print("="*50)
    
    from django.db.models import Sum, Count
    
    try:
        # Пользователи
        user_count = User.objects.count()
        print(f"👤 Пользователей: {user_count}")
        
        # Бюджеты
        budget_count = Budget.objects.count()
        personal_count = Budget.objects.filter(type='personal').count()
        family_count = Budget.objects.filter(type='family').count()
        print(f"💰 Бюджетов: {budget_count} (личных: {personal_count}, семейных: {family_count})")
        
        # Участники бюджетов
        member_count = BudgetMember.objects.count()
        print(f"👥 Участников бюджетов: {member_count}")
        
        # Категории
        category_count = Category.objects.count()
        income_cat_count = Category.objects.filter(type='income').count()
        expense_cat_count = Category.objects.filter(type='expense').count()
        default_cat_count = Category.objects.filter(is_default=True).count()
        print(f"🏷️  Категорий: {category_count}")
        print(f"   • Доходы: {income_cat_count}")
        print(f"   • Расходы: {expense_cat_count}")
        print(f"   • Стандартные: {default_cat_count}")
        
        # Транзакции
        transaction_count = Transaction.objects.count()
        if transaction_count > 0:
            income_sum = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
            expense_sum = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
            income_count = Transaction.objects.filter(type='income').count()
            expense_count = Transaction.objects.filter(type='expense').count()
            
            print(f"💸 Транзакций: {transaction_count}")
            print(f"   • Доходы: {income_count} на сумму {income_sum:.2f}")
            print(f"   • Расходы: {expense_count} на сумму {expense_sum:.2f}")
            print(f"   • Баланс: {(income_sum - expense_sum):.2f}")
        
        print("="*50)
        print("🎉 ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
        
    except Exception as e:
        print(f"❌ Ошибка при выводе статистики: {e}")

def main():
    """Основная функция"""
    print("🚀 ЗАПУСК СКРИПТА ДЛЯ СОЗДАНИЯ ТЕСТОВЫХ ДАННЫХ")
    print("="*60)
    
    try:
        # 1. Создаем пользователей
        users = create_users()
        
        # 2. Создаем бюджеты
        budgets = create_budgets(users)
        
        # 3. Создаем транзакции
        create_transactions(budgets, users)
        
        # 4. Выводим статистику
        print_statistics()
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()