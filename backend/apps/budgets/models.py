"""Модель бюджета пользователя и связанные queryset-методы."""

from django.conf import settings
from django.db import models
from django.db.models import Sum, Q, Count
from decimal import Decimal

class BudgetManager(models.Manager):
    """QuerySet-методы для фильтрации и агрегации бюджетов."""
    
    def personal(self):
        """Фильтр личных бюджетов."""
        return self.filter(type=Budget.TYPE_PERSONAL)
    
    def family(self):
        """Фильтр семейных бюджетов."""
        return self.filter(type=Budget.TYPE_FAMILY)
    
    def by_user(self, user):
        """Получить бюджеты пользователя."""
        return self.filter(owner=user)
    
    def with_transaction_count(self):
        """Аннотировать количество транзакций."""
        return self.annotate(transaction_count=Count('transactions'))


class Budget(models.Model):
    """Бюджет пользователя (личный или семейный)."""
    
    # Choices для типа бюджета
    TYPE_PERSONAL = 'personal'
    TYPE_FAMILY = 'family'
    
    TYPE_CHOICES = [
        (TYPE_PERSONAL, 'Личный'),
        (TYPE_FAMILY, 'Семейный'),
    ]
    
    # Choices для валюты
    CURRENCY_RUB = 'RUB'
    CURRENCY_USD = 'USD'
    CURRENCY_EUR = 'EUR'
    
    CURRENCY_CHOICES = [
        (CURRENCY_RUB, 'Российский рубль (₽)'),
        (CURRENCY_USD, 'Доллар США ($)'),
        (CURRENCY_EUR, 'Евро (€)'),
    ]
    
    name = models.CharField(
        'Название',
        max_length=100,
        help_text='Например: "Мой бюджет", "Семейный бюджет"'
    )
    
    type = models.CharField(
        'Тип бюджета',
        max_length=10,
        choices=TYPE_CHOICES,
        default=TYPE_PERSONAL,
        help_text='Личный или семейный бюджет'
    )
    
    currency = models.CharField(
        'Валюта',
        max_length=3,
        choices=CURRENCY_CHOICES,
        default=CURRENCY_RUB,
        help_text='Валюта по умолчанию для транзакций'
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets',
        verbose_name='Владелец',
        help_text='Пользователь, создавший бюджет'
    )
    
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    
    objects = BudgetManager()

    class Meta:
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'
    
    @property
    def is_personal(self):
        return self.type == self.TYPE_PERSONAL

    @property
    def is_family(self):
        return self.type == self.TYPE_FAMILY
    
    def get_balance(self, date_from=None, date_to=None):
        """
        Баланс бюджета за период (доходы - расходы).

        TODO: Добавить кеширование
        """

        qs = self.transactions.all()

        # Фильтрация по датам 
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)

        # Агрегация
        result = qs.aggregate(
            income=Sum('amount', filter=Q(type='income')),
            expense=Sum('amount', filter=Q(type='expense'))
        )

        income = result['income'] or Decimal('0')
        expense = result['expense'] or Decimal('0')

        return income - expense