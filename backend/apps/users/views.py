"""
ViewSet для работы с пользователями:
регистрация и управление профилем.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer
)
from apps.budgets.models import Budget


class UserViewSet(viewsets.GenericViewSet):
    """
    ViewSet пользователей.

    Реализует регистрацию и работу с профилем текущего пользователя.
    """
    
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от выполняемого action."""

        if self.action == 'register':
            return UserRegistrationSerializer
        elif self.action in ['update_profile', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Возвращает permissions в зависимости от выполняемого action."""
        if self.action == 'register':
            # Регистрация доступна всем
            return [AllowAny()]
        # Остальные действия только для авторизованных
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        Регистрация нового пользователя.
        
        POST /api/users/register/
        
        Ожидает email, пароль и персональные данные.
        Возвращает созданного пользователя или ошибки валидации.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Создаем пользователя после успешной валидации
            user = serializer.save()
            
            # Автоматическое создание личного бюджета
            Budget.objects.create(
                name='Мой бюджет',
                type='personal',
                owner=user
            )
            
            # Возврат данных созданного пользователя
            user_serializer = UserSerializer(user)
            
            return Response({
                'user': user_serializer.data,
                'message': 'Пользователь успешно зарегистрирован'
            }, status=status.HTTP_201_CREATED)
        
        # Возврат ошибок валидации
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get', 'patch'], url_path='profile')
    def profile(self, request):
        """
        Получение и обновление профиля текущего пользователя.

        GET /api/users/profile/ — вернуть данные профиля  
        PATCH /api/users/profile/ — обновить имя и фамилию
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            serializer = UserUpdateSerializer(
                user,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                # Возвращаем полные данные пользователя
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )