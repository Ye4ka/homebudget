"""URL маршруты для приложения Budgets."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.budgets.views import BudgetViewSet

# Создание роутера
router = DefaultRouter()
router.register(r'', BudgetViewSet, basename='budget')

urlpatterns = [
    path('', include(router.urls)),
]
