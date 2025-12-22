"""Админка для приложения Transactions."""
from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Админка для модели Transaction."""
    
    list_display = ['date', 'budget', 'category', 'type', 'amount', 'created_by']
    list_filter = ['type', 'date', 'category']
    search_fields = ['description', 'budget__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'