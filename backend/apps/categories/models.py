from django.db import models

class Category(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    color = models.CharField(max_length=7, default='#000000')
    icon = models.CharField(max_length=50, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'categories'
    
    def __str__(self):
        return self.name