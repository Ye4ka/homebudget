"""ViewSet для работы с транзакциями."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime
from django.db.models import Sum, Count
from decimal import Decimal

from apps.transactions.models import Transaction
from apps.transactions.serializers import (
    TransactionListSerializer,
    TransactionDetailSerializer,
    TransactionCreateUpdateSerializer,
    TransactionStatsSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления транзакциями пользователя.

    Включает:
    - CRUD операции
    - фильтрацию и сортировку
    - получение последних транзакций
    - агрегированную статистику
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Возвращает транзакции пользователя с учётом фильтров.

        Пользователь имеет доступ только к транзакциям своих бюджетов.
        """
        queryset = Transaction.objects.filter(
            budget__owner=self.request.user
        ).select_related(
            'budget',
            'category',
            'created_by'
        )
        
        # Фильтр по бюджету
        budget_id = self.request.query_params.get('budget')
        if budget_id:
            queryset = queryset.filter(budget_id=budget_id)
        
        # Фильтр по типу транзакции
        transaction_type = self.request.query_params.get('type')
        if transaction_type in ['income', 'expense']:
            queryset = queryset.filter(type=transaction_type)
        
        # Фильтр по категории
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Фильтр по датам
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=date_from)
            except ValueError:
                pass  
        
        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=date_to)
            except ValueError:
                pass
        
        # Поиск по описанию и названию категории
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        # Сортировка
        ordering = self.request.query_params.get('ordering', '-date')
        allowed_ordering = ['date', '-date', 'amount', '-amount', 'created_at', '-created_at']
        
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def get_serializer_class(self):
        """Выбирает сериализатор в зависимости от действия."""
        if self.action == 'list':
            return TransactionListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TransactionCreateUpdateSerializer
        elif self.action == 'stats':
            return TransactionStatsSerializer
        else:
            return TransactionDetailSerializer
    
    def perform_create(self, serializer):
        """Создаёт транзакцию от имени текущего пользователя."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='recent')
    def recent(self, request):
        """Возвращает последние 10 транзакций пользователя."""
        queryset = self.get_queryset()[:10]
        serializer = TransactionListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """
        Возвращает агрегированную статистику по транзакциям.

        Поддерживает фильтрацию по бюджету и диапазону дат.
        """
        queryset = self.get_queryset()

        # Подсчёт доходов
        income_data = queryset.filter(type='income').aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        total_income = income_data['total'] or Decimal('0.00')
        income_count = income_data['count']
        
        # Подсчёт расходов
        expense_data = queryset.filter(type='expense').aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        total_expense = expense_data['total'] or Decimal('0.00')
        expense_count = expense_data['count']

        # Вычисление баланса
        balance = total_income - total_expense
        
        # Общее количество транзакций
        transaction_count = queryset.count()

        stats_data = {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'transaction_count': transaction_count,
            'income_count': income_count,
            'expense_count': expense_count,
        }
        
        serializer = TransactionStatsSerializer(stats_data)
        return Response(serializer.data)