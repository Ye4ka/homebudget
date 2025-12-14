"""Админка для приложения Budgets."""
from django.contrib import admin
from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """Админка для модели Budget."""
    
    list_display = ['name', 'type', 'currency', 'owner', 'created_at']
    list_filter = ['type', 'currency', 'created_at']
    search_fields = ['name', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']