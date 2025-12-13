from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    CURRENCY_CHOICES = [
        ('RUB', 'Рубли'),
        ('USD', 'Доллары'),
        ('EUR', 'Евро'),
    ]
    
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='RUB'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  
        related_query_name='custom_user',
    )
    
    class Meta:
        db_table = 'users'
        constraints = [
            models.UniqueConstraint(fields=['username'], name='users_username_key'),
            models.UniqueConstraint(fields=['email'], name='users_email_key'),
        ]
    
    def __str__(self):
        return self.username