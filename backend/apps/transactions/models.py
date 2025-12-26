from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal


class Transaction(models.Model):
    """Транзакция (доход или расход)"""
    
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]
    
    amount = models.DecimalField(
        'Сумма',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    type = models.CharField(
        'Тип транзакции',
        max_length=10,
        choices=TYPE_CHOICES,
        validators=[
            RegexValidator(
                regex='^(income|expense)$',
                message='Тип должен быть income или expense'
            )
        ]
    )
    
    description = models.TextField(
        'Описание',
        blank=True,
        default=''
    )
    
    date = models.DateField('Дата транзакции')
    
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Категория'
    )
    
    budget = models.ForeignKey(
        'budgets.Budget',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Бюджет'
    )
    
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_transactions',
        verbose_name='Создатель'
    )
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['budget', '-date'], name='idx_budget_date'),         
            models.Index(fields=['budget', 'category'], name='idx_budget_category'),   
            models.Index(fields=['type'], name='idx_trans_type'),                      
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name='trans_amount_positive'  
            ),
            models.CheckConstraint(
                check=models.Q(type__in=['income', 'expense']),
                name='trans_valid_type'       
            ),
        ]
    
    def __str__(self):
        return f"{self.type}: {self.amount} ({self.date})"