"""
URL маршруты для HomeBudget API.

Этот модуль определяет главные URL endpoints для проекта.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Django админ-панель
    path('admin/', admin.site.urls),
    
    # JWT Authentication endpoints
    # Получение access и refresh токенов
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Обновление access токена используя refresh токен
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/budgets/', include('apps.budgets.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
]