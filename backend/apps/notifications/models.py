from django.db import models


class Notification(models.Model):
    """Уведомление для пользователя"""
    
    TYPE_CHOICES = [
        ('info', 'Информация'),
        ('warning', 'Предупреждение'),
        ('success', 'Успех'),
        ('error', 'Ошибка'),
    ]
    
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Пользователь'
    )
    
    type = models.CharField(
        'Тип уведомления',
        max_length=20,
        choices=TYPE_CHOICES,
        default='info'
    )
    
    title = models.CharField('Заголовок', max_length=255)
    
    message = models.TextField('Сообщение')
    
    is_read = models.BooleanField('Прочитано', default=False)
    
    related_object_type = models.CharField(
        'Тип связанного объекта',
        max_length=50,
        blank=True,
        null=True
    )
    
    related_object_id = models.PositiveIntegerField(
        'ID связанного объекта',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read'], name='idx_user_read'),  
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(type__in=['info', 'warning', 'success', 'error']),
                name='notif_valid_type'  
            ),
        ]
    
    def __str__(self):
        return f"{self.title} для {self.user.username}"