"""Админка для приложения Categories."""
from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Category."""
    
    list_display = ['name', 'type', 'color', 'icon', 'is_system', 'created_at']
    list_filter = ['type', 'is_system']
    search_fields = ['name']
    readonly_fields = ['created_at']