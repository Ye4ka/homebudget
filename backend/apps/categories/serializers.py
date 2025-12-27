"""Сериализаторы для приложения Categories."""
from rest_framework import serializers
from apps.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями."""
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    transaction_count = serializers.SerializerMethodField()
    can_be_deleted = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'type',
            'type_display',
            'icon',
            'color',
            'is_system',
            'transaction_count',
            'can_be_deleted',
            'created_at',
        ]
        read_only_fields = ['id', 'is_system', 'created_at']
    
    def get_transaction_count(self, obj):
        """
        Получить количество транзакций.
        Сначала пробуем взять из аннотации, если нет - из property.
        """
        if hasattr(obj, '_transaction_count'):
            return obj._transaction_count
        
        if hasattr(obj, '__dict__') and 'transaction_count' in obj.__dict__:
            return obj.__dict__['transaction_count']
        
        return obj.transaction_count
    
    def get_can_be_deleted(self, obj):
        """Можно ли удалить категорию."""
        return obj.can_be_deleted
    
    def validate_name(self, value):
        """Валидация названия категории."""
        value = value.strip()
        
        if len(value) < 2:
            raise serializers.ValidationError(
                'Название должно содержать минимум 2 символа'
            )
        
        if len(value) > 50:
            raise serializers.ValidationError(
                'Название не должно превышать 50 символов'
            )
        
        return value
    
    def validate_icon(self, value):
        """Валидация иконки."""
        value = value.strip()
        
        if not value[0].isupper():
            raise serializers.ValidationError(
                'Название иконки должно начинаться с заглавной буквы'
            )
        
        return value
    
    def validate_color(self, value):
        """Валидация HEX цвета."""
        if not value.startswith('#'):
            raise serializers.ValidationError(
                'Цвет должен начинаться с #'
            )
        
        if len(value) != 7:
            raise serializers.ValidationError(
                'Цвет должен быть в формате #RRGGBB'
            )
        
        return value.upper()  
    
    def validate(self, attrs):
        """Проверка уникальности категории."""
        name = attrs.get('name')
        category_type = attrs.get('type')
        
        instance = self.instance
        
        qs = Category.objects.filter(name=name, type=category_type)
        
        if instance:
            qs = qs.exclude(pk=instance.pk)
        
        if qs.exists():
            raise serializers.ValidationError({
                'name': f'Категория "{name}" с типом "{category_type}" уже существует'
            })
        
        return attrs


class CategoryListSerializer(serializers.ModelSerializer):
    """Облегчённый сериализатор для списка категорий."""
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'type',
            'type_display',
            'icon',
            'color',
            'is_system',
        ]