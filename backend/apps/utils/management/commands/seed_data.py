from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.categories.models import Category
from apps.budgets.models import Budget, BudgetMember
from apps.transactions.models import Transaction
from datetime import datetime, timedelta
import random
import decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Создать все тестовые данные для проекта'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--transactions',
            type=int,
            default=50,
            help='Количество транзакций для создания (по умолчанию 50)'
        )
    
    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("🚀 СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ ДЛЯ ЗАДАЧИ 2")
        self.stdout.write("=" * 60)
        
        num_transactions = options['transactions']
        
        # 1. Суперпользователь
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_superuser': True,
                'is_staff': True,
                'currency': 'RUB'
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('✅ Суперпользователь admin создан'))
        
        # 2. Категории (12 штук)
        categories_data = [
            # Доходы
            {"name": "Зарплата", "type": "income", "color": "#4CAF50", "icon": "wallet"},
            {"name": "Фриланс", "type": "income", "color": "#8BC34A", "icon": "laptop"},
            {"name": "Инвестиции", "type": "income", "color": "#CDDC39", "icon": "chart-line"},
            {"name": "Подарки", "type": "income", "color": "#FFEB3B", "icon": "gift"},
            {"name": "Возврат долгов", "type": "income", "color": "#FFC107", "icon": "hand-holding-usd"},
            {"name": "Прочие доходы", "type": "income", "color": "#FF9800", "icon": "ellipsis-h"},
            
            # Расходы
            {"name": "Продукты", "type": "expense", "color": "#F44336", "icon": "shopping-cart"},
            {"name": "Транспорт", "type": "expense", "color": "#E91E63", "icon": "car"},
            {"name": "Жилье", "type": "expense", "color": "#9C27B0", "icon": "home"},
            {"name": "Развлечения", "type": "expense", "color": "#673AB7", "icon": "film"},
            {"name": "Здоровье", "type": "expense", "color": "#3F51B5", "icon": "heartbeat"},
            {"name": "Образование", "type": "expense", "color": "#2196F3", "icon": "graduation-cap"},
        ]
        
        for data in categories_data:
            Category.objects.get_or_create(
                name=data['name'],
                type=data['type'],
                is_default=True,
                defaults={
                    'color': data['color'],
                    'icon': data['icon'],
                    'created_by': admin
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✅ 12 категорий создано (6 доходов, 6 расходов)'))
        
        # 3. Тестовые пользователи (3 штуки)
        test_users = []
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
                self.stdout.write(self.style.SUCCESS(f'✅ Пользователь {user.username} создан'))
            else:
                self.stdout.write(f'⚠️  Пользователь {user.username} уже существует')
            test_users.append(user)
        
        # 4. Бюджеты (2 штуки)
        personal_budget, created = Budget.objects.get_or_create(
            name='Личный бюджет Алекса',
            defaults={
                'type': 'personal',
                'owner': test_users[0],
                'currency': test_users[0].currency
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Личный бюджет создан'))
        
        family_budget, created = Budget.objects.get_or_create(
            name='Семейный бюджет',
            defaults={
                'type': 'family',
                'owner': test_users[0],
                'currency': 'RUB'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Семейный бюджет создан'))
            
            # Добавляем участников
            for user in test_users[1:]:
                BudgetMember.objects.create(
                    budget=family_budget,
                    user=user,
                    role='editor'
                )
                self.stdout.write(f'✅ Участник {user.username} добавлен в семейный бюджет')
        
        # 5. Транзакции
        income_cats = list(Category.objects.filter(type='income'))
        expense_cats = list(Category.objects.filter(type='expense'))
        today = datetime.now().date()
        
        for i in range(num_transactions):
            # Выбираем случайный бюджет
            budget = random.choice([personal_budget, family_budget])
            
            # 70% расходы, 30% доходы
            if random.random() < 0.7:
                trans_type = 'expense'
                amount = decimal.Decimal(random.uniform(100, 5000)).quantize(decimal.Decimal('0.01'))
                category = random.choice(expense_cats)
            else:
                trans_type = 'income'
                amount = decimal.Decimal(random.uniform(1000, 20000)).quantize(decimal.Decimal('0.01'))
                category = random.choice(income_cats)
            
            # Случайная дата за последние 90 дней
            days_ago = random.randint(0, 90)
            trans_date = today - timedelta(days=days_ago)
            
            # Кто создал транзакцию
            if budget.type == 'personal':
                created_by = budget.owner
            else:
                # Для семейного бюджета - случайный участник
                created_by = random.choice(test_users)
            
            Transaction.objects.create(
                amount=amount,
                type=trans_type,
                description=f'Тестовая транзакция #{i+1}',
                date=trans_date,
                category=category,
                budget=budget,
                created_by=created_by
            )
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'  Создано {i + 1} транзакций...')
        
        self.stdout.write(self.style.SUCCESS(f'✅ {num_transactions} транзакций создано'))
        
        # 6. Статистика
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 СТАТИСТИКА СОЗДАННЫХ ДАННЫХ")
        self.stdout.write("=" * 60)
        
        from django.db.models import Sum
        
        transaction_count = Transaction.objects.count()
        income_sum = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense_sum = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        self.stdout.write(f"👤 Пользователей: {User.objects.count()}")
        self.stdout.write(f"💰 Бюджетов: {Budget.objects.count()}")
        self.stdout.write(f"🏷️  Категорий: {Category.objects.count()}")
        self.stdout.write(f"💸 Транзакций: {transaction_count}")
        self.stdout.write(f"📈 Сумма доходов: {income_sum:.2f}")
        self.stdout.write(f"📉 Сумма расходов: {expense_sum:.2f}")
        self.stdout.write(f"⚖️  Баланс: {income_sum - expense_sum:.2f}")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("🎉 ЗАДАЧА 2 ВЫПОЛНЕНА УСПЕШНО!"))
        self.stdout.write("=" * 60)
        
        self.stdout.write("\n✅ ЧТО БЫЛО СДЕЛАНО:")
        self.stdout.write("   • 12 категорий (6 доходов + 6 расходов)")
        self.stdout.write("   • 3 тестовых пользователя")
        self.stdout.write("   • 2 бюджета (личный и семейный)")
        self.stdout.write(f"   • {num_transactions} транзакций")
        self.stdout.write("   • Все CHECK constraints добавлены в миграциях")