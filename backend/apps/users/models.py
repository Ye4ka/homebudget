"""Кастомная модель пользователя и менеджер для аутентификации по email."""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Менеджер пользователей с поддержкой аутентификации по email
    и корректного создания суперпользователей.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт пользователя с email в качестве логина.
        Email нормализуется, пароль хешируется.
        """
        if not email:
            raise ValueError('Email адрес обязателен')
        
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        
        user.set_password(password)
        
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт суперпользователя с обязательными флагами is_staff и is_superuser."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Проверяем что флаги установлены
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя с аутентификацией по email."""
    
    email = models.EmailField(
        'Email адрес',
        unique=True,
        help_text='Используется для входа в систему'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False
    )
    is_active = models.BooleanField(
        'Активен',
        default=True,
        help_text='Отметьте, если пользователь должен иметь доступ к системе'
    )
    is_staff = models.BooleanField(
        'Персонал',
        default=False,
        help_text='Отметьте, если пользователь может входить в админ-панель'
    )
    date_joined = models.DateTimeField(
        'Дата регистрации',
        auto_now_add=True
    )
    
    objects = UserManager()
    
    # Используем email как уникальный идентификатор вместо username
    USERNAME_FIELD = 'email'
    
    # Обязательные поля при создании суперпользователя
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']  # Сортировка по дате
        app_label = 'users'
    def __str__(self):
        """Строковое представление пользователя."""
        return self.email
    
    def get_full_name(self):
        """Получить полное имя пользователя."""
        return f'{self.first_name} {self.last_name}'
    
    def get_short_name(self):
        """Получить короткое имя (только имя)."""
        return self.first_name
    
    @property
    def full_name(self):
        """Полное имя пользователя."""
        return self.get_full_name()
    
    @property
    def initials(self):
        """Получить инициалы пользователя."""
        first_initial = self.first_name[0].upper() if self.first_name else ''
        last_initial = self.last_name[0].upper() if self.last_name else ''
        return f'{first_initial}{last_initial}'
    
    @property
    def budget_count(self):
        """Количество бюджетов пользователя."""
        return self.budgets.count()
    
    @property
    def has_budgets(self):
        """Проверить есть ли у пользователя бюджеты."""
        return self.budgets.exists()    