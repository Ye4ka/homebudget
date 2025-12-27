"""Сериализаторы для приложения Transaction."""
from rest_framework import serializers
from apps.transactions.models import Transaction
from apps.categories.serializers import CategoryListSerializer


class TransactionListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка транзакций.
    Включает вложенную информацию о категории.
    """
    
    category = CategoryListSerializer(read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    formatted_amount = serializers.CharField(read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'budget',
            'category',
            'type',
            'type_display',
            'amount',
            'formatted_amount',
            'description',
            'date',
            'created_by',
            'created_by_name',
            'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']
    
    def get_created_by_name(self, obj):
        """Получить имя создателя транзакции."""
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
        return "Неизвестно"


class TransactionDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о транзакции."""
    
    category = CategoryListSerializer(read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    created_by_name = serializers.SerializerMethodField()
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    
    formatted_amount = serializers.CharField(read_only=True)
    signed_amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'budget',
            'category',
            'type',
            'type_display',
            'amount',
            'formatted_amount',
            'signed_amount',
            'description',
            'date',
            'created_by',
            'created_by_name',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_created_by_name(self, obj):
        """Получить имя создателя."""
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
        return "Неизвестно"


class TransactionCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления транзакции."""
    
    class Meta:
        model = Transaction
        fields = [
            'budget',
            'category',
            'type',
            'amount',
            'description',
            'date',
        ]
    
    def validate_amount(self, value):
        """Проверка, что сумма транзакции положительная"""
        if value <= 0:
            raise serializers.ValidationError(
                'Сумма должна быть больше нуля'
            )
        return value
    
    def validate(self, attrs):
        """Проверка соответствия типа категории и транзакции."""
        category = attrs.get('category')
        transaction_type = attrs.get('type')
        
        if category and transaction_type:
            if transaction_type == 'income' and category.type != 'income':
                raise serializers.ValidationError({
                    'category': f'Категория "{category.name}" предназначена для расходов. '
                            'Выберите категорию для доходов.'
                })
            elif transaction_type == 'expense' and category.type != 'expense':
                raise serializers.ValidationError({
                    'category': f'Категория "{category.name}" предназначена для доходов. '
                            'Выберите категорию для расходов.'
                })
        
        return attrs


class TransactionStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики по транзакциям."""
    
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    income_count = serializers.IntegerField()
    expense_count = serializers.IntegerField()