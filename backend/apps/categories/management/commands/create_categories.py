from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.categories.models import Category

User = get_user_model()

class Command(BaseCommand):
    help = 'Создать стандартные категории доходов и расходов'
    
    def handle(self, *args, **options):
        self.stdout.write("📦 Создание стандартных категорий...")
        
       
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_superuser': True,
                'is_staff': True,
                'currency': 'RUB'
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✅ Суперпользователь создан'))
        
        categories = [
            # Доходы (6 категорий)
            {"name": "Зарплата", "type": "income", "color": "#4CAF50", "icon": "account-balance-wallet"},
            {"name": "Фриланс", "type": "income", "color": "#8BC34A", "icon": "laptop"},
            {"name": "Инвестиции", "type": "income", "color": "#CDDC39", "icon": "trending-up"},
            {"name": "Подарки", "type": "income", "color": "#FFEB3B", "icon": "card-giftcard"},
            {"name": "Возврат долгов", "type": "income", "color": "#FFC107", "icon": "handshake"},
            {"name": "Прочие доходы", "type": "income", "color": "#FF9800", "icon": "more-horiz"},
            
            # Расходы (6 категорий)
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
                    created_by=admin_user
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Создана: {cat_data["name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Ошибка создания {cat_data["name"]}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Категории созданы: {created_count} новых, {existing_count} уже существовало'))
        self.stdout.write(f'📊 Всего категорий в БД: {Category.objects.count()}')
        
        # Статистика
        income_cats = Category.objects.filter(type='income', is_default=True).count()
        expense_cats = Category.objects.filter(type='expense', is_default=True).count()
        self.stdout.write(f'   • Доходы: {income_cats} категорий')
        self.stdout.write(f'   • Расходы: {expense_cats} категорий')