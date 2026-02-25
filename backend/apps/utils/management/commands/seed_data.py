from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from categories.models import Category
from budgets.models import Budget
from transactions.models import Transaction
import random
import decimal
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Создание тестовых данных'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Создание тестовых данных...'))
        
        # 1. Пользователь
        User = get_user_model()
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'Тест',
                'last_name': 'Пользователь'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'✅ Создан пользователь: {user.email}')
        
        # 2. Бюджет
        budget, created = Budget.objects.get_or_create(
            name='Тестовый бюджет',
            owner=user,
            defaults={'type': 'personal', 'currency': 'RUB'}
        )
        self.stdout.write(f'✅ Бюджет: {budget.name}')
        
        # 3. Категории
        if Category.objects.count() == 0:
            Category.objects.create(name='Зарплата', type='income', color='#10B981', icon='Money', is_system=True)
            Category.objects.create(name='Продукты', type='expense', color='#EF4444', icon='Cart', is_system=True)
            self.stdout.write('✅ Созданы базовые категории')
        
        # 4. Транзакции
        for i in range(10):
            days_ago = random.randint(0, 30)
            date = datetime.now().date() - timedelta(days=days_ago)
            category = random.choice(list(Category.objects.all()))
            
            Transaction.objects.create(
                budget=budget,
                category=category,
                type=category.type,
                amount=decimal.Decimal(str(round(random.uniform(100, 5000), 2))),
                description=f'Транзакция #{i+1}',
                date=date,
                created_by=user
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные созданы!'))
        self.stdout.write(f'   Логин: test@example.com / password123')
