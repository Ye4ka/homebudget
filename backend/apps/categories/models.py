"""Модель категорий доходов и расходов."""

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
import re

def validate_hex_color(value):
    """Проверка HEX цвета (#RRGGBB)."""
    hex_pattern = r'^#([A-Fa-f0-9]{6})$'
    if not re.match(hex_pattern, value):
        raise ValidationError(
            f'{value} не является корректным HEX цветом. '
            'Используйте формат #RRGGBB (например: #EF4444)'
        )

class Category(models.Model):
    """Категория доходов или расходов."""
    
    # Choices для типа категории
    TYPE_INCOME = 'income'
    TYPE_EXPENSE = 'expense'
    
    TYPE_CHOICES = [
        (TYPE_INCOME, 'Доход'),
        (TYPE_EXPENSE, 'Расход'),
    ]
    
    name = models.CharField(
        'Название',
        max_length=50,
        help_text='Например: "Продукты", "Зарплата"'
    )
    
    type = models.CharField(
        'Тип',
        max_length=10,
        choices=TYPE_CHOICES,
        help_text='Категория для доходов или расходов'
    )
    
    icon = models.CharField(
        'Иконка',
        max_length=50,
        help_text='Идентификатор иконки'
    )
    
    color = models.CharField(
        'Цвет',
        max_length=7,
        validators=[validate_hex_color],
        help_text='Цвет в HEX формате (например: #EF4444)'
    )
    
    is_system = models.BooleanField(
        'Системная категория',
        default=False,
        help_text='Системные категории нельзя удалить'
    )
    
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['type', 'name']
        
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_category_name_type'
            )
        ]
    
    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'
    
    @property
    def is_income(self):
        """Является ли категория доходной."""
        return self.type == self.TYPE_INCOME
    
    @property
    def is_expense(self):
        """Является ли категория расходной."""
        return self.type == self.TYPE_EXPENSE
    
    @property
    def transaction_count(self):
        """Количество транзакций в этой категории."""
        return self.transactions.count()

    @property
    def can_be_deleted(self):
        """Проверить можно ли удалить категорию"""
        return not self.is_system and not self.transactions.exists()
    
    # Методы валидации
    
    def clean(self):
        """Дополнительная бизнес-валидация категории."""
        errors = {}
        
        # Валидация названия
        if self.name:
            self.name = self.name.strip()
            
            if len(self.name) < 2:
                errors['name'] = 'Название должно быть минимум 2 символа'
        
        # Валидация иконки 
        if self.icon:
            self.icon = self.icon.strip()
            if not self.icon[0].isupper():
                errors['icon'] = 'Название иконки должно начинаться с заглавной буквы.'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        """Сохранение с обязательным вызовом full_clean()."""
        self.full_clean()
        super().save(*args, **kwargs)