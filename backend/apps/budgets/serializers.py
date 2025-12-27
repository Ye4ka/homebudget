"""Сериализаторы для приложения Budgets."""
from rest_framework import serializers
from apps.budgets.models import Budget


class BudgetListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка бюджетов."""
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = [
            'id',
            'name',
            'type',
            'type_display',
            'currency',
            'currency_display',
            'owner_email',
            'owner_name',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_owner_name(self, obj):
        """Получить полное имя владельца."""
        return f"{obj.owner.first_name} {obj.owner.last_name}".strip()


class BudgetDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о бюджете."""

    type_display = serializers.CharField(source='get_type_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_name = serializers.SerializerMethodField()
    
    balance = serializers.SerializerMethodField()
    transaction_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Budget
        fields = [
            'id',
            'name',
            'type',
            'type_display',
            'currency',
            'currency_display',
            'owner',
            'owner_email',
            'owner_name',
            'balance',
            'transaction_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_owner_name(self, obj):
        """Получить полное имя владельца."""
        return f"{obj.owner.first_name} {obj.owner.last_name}".strip()
    
    def get_balance(self, obj):
        """Получить текущий баланс бюджета."""
        balance = obj.get_balance()
        return float(balance)


class BudgetCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления бюджета."""
    
    class Meta:
        model = Budget
        fields = [
            'name',
            'type',
            'currency',
            'id',
        ]
        read_only_fields = ['id']
    
    def validate_name(self, value):
        """Валидация названия бюджета."""
        value = value.strip()
        
        # Проверка минимальной длины
        if len(value) < 2:
            raise serializers.ValidationError(
                'Название должно содержать минимум 2 символа'
            )
        
        # Проверка максимальной длины
        if len(value) > 100:
            raise serializers.ValidationError(
                'Название не должно превышать 100 символов'
            )
        
        return value
    

class BudgetSummarySerializer(serializers.Serializer):
    """Сериализатор для сводной информации о бюджете."""
    
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    currency = serializers.CharField()
    period_start = serializers.DateField(allow_null=True)
    period_end = serializers.DateField(allow_null=True)