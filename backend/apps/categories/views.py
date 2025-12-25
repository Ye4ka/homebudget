"""ViewSet для работы с категориями транзакций."""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count

from apps.categories.models import Category
from apps.categories.serializers import (
    CategorySerializer,
    CategoryListSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления категориями пользователя.

    Включает:
    - список категорий с фильтрацией
    - создание пользовательских категорий
    - обновление и удаление пользовательских категорий
    - защиту системных категорий от изменений
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Возвращает категории с аннотацией количества транзакций."""
        permission_classes = [IsAuthenticated]
        
        queryset = Category.objects.all()
        
        # Фильтрация по типу
        category_type = self.request.query_params.get('type')
        if category_type in ['income', 'expense']:
            queryset = queryset.filter(type=category_type)
        
        # Фильтрация по системным категориям
        is_system = self.request.query_params.get('is_system')
        if is_system == 'true':
            queryset = queryset.filter(is_system=True)
        elif is_system == 'false':
            queryset = queryset.filter(is_system=False)
        
        return queryset
    
    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от выполняемого action."""
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer
    
    def perform_create(self, serializer):
        """Создание пользовательской категории."""
        serializer.save(is_system=False)
    
    def perform_update(self, serializer):
        """
        Обновление категории.
        Системные категории нельзя изменять.
        """
        if self.get_object().is_system:
            raise PermissionDenied("Системные категории нельзя изменять")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Удаление категории.
        Проверка:
        1. Не системная ли категория
        2. Нет ли транзакций в этой категории
        """
        if instance.is_system:
            raise PermissionDenied("Системные категории нельзя удалять")
        
        if instance.transactions.exists():
            return Response(
                {
                    'error': 'Нельзя удалить категорию с транзакциями',
                    'transaction_count': instance.transactions.count()
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.delete()