from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Goal(models.Model):
    """Финансовая цель"""
    
    STATUS_CHOICES = [
        ('active', 'Активная'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    name = models.CharField('Название цели', max_length=255)
    
    target_amount = models.DecimalField(
        'Целевая сумма',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    current_amount = models.DecimalField(
        'Текущая сумма',
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    deadline = models.DateField('Срок выполнения', null=True, blank=True)
    
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    budget = models.ForeignKey(
        'budgets.Budget',
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='Бюджет'
    )
    
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_goals',
        verbose_name='Создатель'
    )
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        constraints = [
            models.CheckConstraint(
                check=models.Q(target_amount__gt=0),
                name='goal_target_amount_positive'
            ),
            models.CheckConstraint(
                check=models.Q(current_amount__gte=0),
                name='goal_current_amount_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(status__in=['active', 'completed', 'cancelled']),
                name='goal_valid_status'
            ),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.current_amount}/{self.target_amount})"
    
    def progress_percentage(self):
        """Процент выполнения цели"""
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100