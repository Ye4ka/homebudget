"""Модель транзакций доходов и расходов и менеджер для аналитических запросов."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, Q, Count
from decimal import Decimal
from datetime import date

class TransactionManager(models.Manager):
    """QuerySet-методы для фильтрации и агрегации транзакций."""
    
    def income(self):
        """Получить только доходы."""
        return self.filter(type=Transaction.TYPE_INCOME)
    
    def expense(self):
        """Получить только расходы."""
        return self.filter(type=Transaction.TYPE_EXPENSE)
    
    def by_budget(self, budget):
        """Фильтр транзакций по бюджету."""
        return self.filter(budget=budget)
    
    def by_category(self, category):
        """Получить транзакции категории."""
        return self.filter(category=category)
    
    def by_date_range(self, date_from=None, date_to=None):
        """Фильтр транзакций по диапазону дат."""
        qs = self.all()
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs
    
    def current_month(self):
        """Получить транзакции текущего месяца."""
        today = date.today()
        return self.filter(
            date__year=today.year,
            date__month=today.month
        )
    
    def total_income(self):
        """Сумма доходов (возвращает Decimal('0') при отсутствии данных)."""
        result = self.income().aggregate(total=Sum('amount'))
        return result['total'] or Decimal('0')
    
    def total_expense(self):
        """Сумма расходов (возвращает Decimal('0') при отсутствии данных)."""
        result = self.expense().aggregate(total=Sum('amount'))
        return result['total'] or Decimal('0')


class Transaction(models.Model):
    """Запись о доходе или расходе в бюджете."""
    
    # Choices для типа транзакции
    TYPE_INCOME = 'income'
    TYPE_EXPENSE = 'expense'
    
    TYPE_CHOICES = [
        (TYPE_INCOME, 'Доход'),
        (TYPE_EXPENSE, 'Расход'),
    ]

    CURRENCY_SYMBOLS = {
        'RUB': '₽',
        'USD': '$',
        'EUR': '€',
    }
    
    budget = models.ForeignKey(
        'budgets.Budget',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Бюджет'
    )
    
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,  # Нельзя удалить категорию если есть транзакции
        related_name='transactions',
        verbose_name='Категория'
    )
    
    type = models.CharField(
        'Тип',
        max_length=10,
        choices=TYPE_CHOICES
    )
    
    amount = models.DecimalField(
        'Сумма',
        max_digits=10,
        decimal_places=2,
        help_text='Сумма транзакции'
    )
    
    description = models.TextField(
        'Описание',
        blank=True,
        help_text='Опциональное описание транзакции'
    )
    
    date = models.DateField(
        'Дата',
        help_text='Дата когда произошла транзакция'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions',
        verbose_name='Создатель'
    )
    
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )

    objects = TransactionManager()
    
    class Meta:
        app_label = 'transactions' 
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date', '-created_at']
        
        # Индексы для быстрых запросов
        indexes = [
            models.Index(fields=['budget', '-date']),
            models.Index(fields=['budget', 'category']),
            models.Index(fields=['type']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        sign = '+' if self.type == self.TYPE_INCOME else '-'
        return f'{sign}{self.amount} {self.budget.currency} - {self.category.name}'
    
    @property
    def is_income(self):
        """Является ли транзакция доходной."""
        return self.type == self.TYPE_INCOME
    
    @property
    def is_expense(self):
        """Является ли транзакция расходной."""
        return self.type == self.TYPE_EXPENSE
    
    @property
    def signed_amount(self):
        """
        Сумма с учётом типа транзакции:
        доход - положительная, расход - отрицательная.
        """
        return self.amount if self.is_income else -self.amount
    
    @property
    def formatted_amount(self):
        """Отформатированная сумма с валютой и знаком (+ / -)."""
        sign = '+' if self.is_income else '-'
        # Форматирование с разделителями тысяч
        amount_str = f'{self.amount:,.2f}'.replace(',', ' ')

        symbol = settings.CURRENCY_SYMBOLS.get(
            self.budget.currency, 
            self.budget.currency
        )
        
        return f'{sign}{amount_str} {symbol}'
    
    def clean(self):
        """Дополнительная бизнес-валидация транзакции."""

        errors = {}

        # Проверка суммы
        if self.amount and self.amount <= 0:
            errors['amount'] = 'Сумма должна быть больше нуля'

        # Проверка соответствия типа категории и транзакции
        if self.category and self.type:
            if self.type == self.TYPE_INCOME and self.category.type != 'income':
                errors['category'] = (
                    f'Категория "{self.category.name}" предназначена для расходов. '
                    'Выберите категорию для доходов.'
                )
            elif self.type == self.TYPE_EXPENSE and self.category.type != 'expense':
                errors['category'] = (
                    f'Категория "{self.category.name}" предназначена для доходов. '
                    'Выберите категорию для расходов.'
                )
    
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        """Сохранение с обязательным вызовом full_clean()."""
        self.full_clean()
        super().save(*args, **kwargs)