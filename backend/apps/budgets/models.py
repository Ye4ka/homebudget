from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator


class Budget(models.Model):
    """Бюджет (личный или семейный)"""
    
    BUDGET_TYPES = [
        ('personal', 'Личный'),
        ('family', 'Семейный'),
    ]
    
    CURRENCY_CHOICES = [
        ('RUB', 'Рубль'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
        ('KZT', 'Тенге'),
    ]
    
    name = models.CharField(
        'Название бюджета',
        max_length=255,
        validators=[MinLengthValidator(1)]
    )
    
    type = models.CharField(
        'Тип бюджета',
        max_length=20,
        choices=BUDGET_TYPES,
        default='personal',
        validators=[
            RegexValidator(
                regex='^(personal|family)$',
                message='Тип должен быть personal или family'
            )
        ]
    )
    
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='owned_budgets',
        verbose_name='Владелец'
    )
    
    currency = models.CharField(
        'Валюта бюджета',
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='RUB',
        validators=[
            RegexValidator(
                regex='^(RUB|USD|EUR|KZT)$',
                message='Валюта должна быть RUB, USD, EUR или KZT'
            )
        ]
    )
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'
        constraints = [
            models.CheckConstraint(
                check=models.Q(type__in=['personal', 'family']),
                name='budget_valid_type'  # уже короткое
            ),
            models.CheckConstraint(
                check=models.Q(currency__in=['RUB', 'USD', 'EUR', 'KZT']),
                name='budget_valid_curr'  # сокращено
            ),
            models.UniqueConstraint(
                fields=['owner', 'name'],
                name='unique_budget_name'  # сокращено
            ),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class BudgetMember(models.Model):
    """Участник семейного бюджета"""
    
    ROLE_CHOICES = [
        ('owner', 'Владелец'),
        ('editor', 'Редактор'),
        ('viewer', 'Наблюдатель'),
    ]
    
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Бюджет'
    )
    
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='budget_memberships',
        verbose_name='Пользователь'
    )
    
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer'
    )
    
    joined_at = models.DateTimeField('Дата присоединения', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Участник бюджета'
        verbose_name_plural = 'Участники бюджетов'
        unique_together = ['budget', 'user']
        constraints = [
            models.CheckConstraint(
                check=models.Q(role__in=['owner', 'editor', 'viewer']),
                name='bm_valid_role'  # сокращено
            ),
        ]
    
    def __str__(self):
        return f"{self.user.username} в {self.budget.name}"