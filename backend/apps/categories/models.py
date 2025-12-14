from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator


class Category(models.Model):
    """Категория доходов/расходов"""
    
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]
    
    name = models.CharField(
        'Название категории',
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    
    type = models.CharField(
        'Тип',
        max_length=10,
        choices=TYPE_CHOICES,
        validators=[
            RegexValidator(
                regex='^(income|expense)$',
                message='Тип должен быть income или expense'
            )
        ]
    )
    
    color = models.CharField(
        'Цвет',
        max_length=7,
        default='#3B82F6',
        validators=[
            RegexValidator(
                regex='^#[0-9A-Fa-f]{6}$',
                message='Цвет должен быть в HEX формате (#RRGGBB)'
            )
        ]
    )
    
    icon = models.CharField(
        'Иконка',
        max_length=50,
        default='category',
        help_text='Название иконки из Material Design Icons'
    )
    
    is_default = models.BooleanField(
        'Стандартная категория',
        default=False,
        help_text='Стандартные категории доступны всем пользователям'
    )
    
    budget = models.ForeignKey(
        'budgets.Budget',
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True,
        verbose_name='Бюджет',
        help_text='Если NULL - стандартная категория'
    )
    
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_categories',
        verbose_name='Создатель'
    )
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.CheckConstraint(
                check=models.Q(type__in=['income', 'expense']),
                name='cat_valid_type'  
            ),
            models.UniqueConstraint(
                condition=models.Q(budget__isnull=False),
                fields=['name', 'budget'],
                name='unique_cat_per_budget'  
            ),
            models.UniqueConstraint(
                condition=models.Q(budget__isnull=True, is_default=True),
                fields=['name'],
                name='unique_default_cat'  
            ),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"