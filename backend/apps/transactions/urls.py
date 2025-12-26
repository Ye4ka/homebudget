"""URL маршруты для приложения Transactions."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.transactions.views import TransactionViewSet

# Создание роутера
router = DefaultRouter()
router.register(r'', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]