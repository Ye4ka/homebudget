from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Пользователь системы"""
    
    CURRENCY_CHOICES = [
        ('RUB', 'Рубль'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
        ('KZT', 'Тенге'),
    ]
    
    email = models.EmailField(
        'Email адрес',
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует.',
        }
    )
    
    currency = models.CharField(
        'Валюта по умолчанию',
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
    

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']  
    
    def __str__(self):
        return self.username