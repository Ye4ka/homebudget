"""ViewSet для работы с бюджетами."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q, Count
from decimal import Decimal
from datetime import datetime

from apps.budgets.models import Budget
from apps.budgets.serializers import (
    BudgetListSerializer,
    BudgetDetailSerializer,
    BudgetCreateUpdateSerializer,
    BudgetSummarySerializer,
)


class BudgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления бюджетами пользователя.

    Включает:
    - список бюджетов
    - создание, обновление и удаление
    - получение сводной информации по бюджету
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Возвращает бюджеты текущего пользователя с количеством транзакций."""
        return Budget.objects.filter(
            owner=self.request.user
        ).annotate(
            transaction_count=Count('transactions')
        ).select_related('owner')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BudgetListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BudgetCreateUpdateSerializer
        elif self.action == 'summary':
            return BudgetSummarySerializer
        else:
            return BudgetDetailSerializer
    
    def perform_create(self, serializer):
        """Создание бюджета с привязкой к текущему пользователю."""
        serializer.save(owner=self.request.user)
    
    def perform_destroy(self, instance):
        """Удаление бюджета."""
        instance.delete()
    
    @action(detail=True, methods=['get'], url_path='summary')
    def summary(self, request, pk=None):
        """Сводная информация по бюджету за период."""
        budget = self.get_object()
        
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        try:
            if date_from:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            if date_to:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Неверный формат даты. Используйте YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qs = budget.transactions.all()
        
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        
        result = qs.aggregate(
            total_income=Sum('amount', filter=Q(type='income')),
            total_expense=Sum('amount', filter=Q(type='expense')),
            transaction_count=Count('id')
        )
        
        total_income = result['total_income'] or Decimal('0')
        total_expense = result['total_expense'] or Decimal('0')
        balance = total_income - total_expense
        
        summary_data = {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'transaction_count': result['transaction_count'],
            'currency': budget.currency,
            'period_start': date_from,
            'period_end': date_to,
        }
        
        serializer = BudgetSummarySerializer(summary_data)
        return Response(serializer.data)