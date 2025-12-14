"""Сериализаторы для приложения Users."""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Подтверждение пароля'
    )
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        """
        Валидация данных регистрации.
        
        Проверяет что пароли совпадают.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': 'Пароли не совпадают'
            })
        
        return attrs
    
    def create(self, validated_data):
        """
        Создать нового пользователя.

        Удаляет password2 и создаёт пользователя через менеджер.
        """
        validated_data.pop('password2')
        
        user = User.objects.create_user(**validated_data)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения данных пользователя.
    
    Используется для профиля и списка пользователей.
    """
    
    full_name = serializers.CharField(read_only=True)
    initials = serializers.CharField(read_only=True)
    budget_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'initials',
            'budget_count',
            'date_joined',
        ]
        read_only_fields = ['id', 'email', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля пользователя.
    
    Позволяет менять только имя и фамилию.
    """
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']