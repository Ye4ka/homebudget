# HomeBudget Backend

Django REST API для управления личными и семейными финансами.

##  Технологии

- **Python 3.11+** — язык программирования
- **Django 5.2** — веб-фреймворк
- **Django REST Framework 3.16** — построение REST API
- **PostgreSQL 15+** — реляционная база данных (production)
- **SQLite** — база данных для разработки (development)
- **JWT (Simple JWT)** — аутентификация через токены
- **django-cors-headers** — поддержка CORS для Frontend
- **django-filter** — фильтрация данных в API
- **Pillow** — обработка изображений (аватары пользователей)
- **Pandas** — работа с CSV/Excel файлами
- **ReportLab** — генерация PDF отчётов
- **python-dotenv** — управление переменными окружения

## Требования

- **Python 3.11** или выше
- **PostgreSQL 15** или выше (для production)
- **pip** — менеджер пакетов Python

##  Установка и запуск

### 1. Клонирование репозитория
```bash
# Клонировать репозиторий
git clone 

# Перейти в папку backend
cd homebudget/backend
```

### 2. Создание виртуального окружения
```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
# Обновить pip до последней версии
pip install --upgrade pip

# Установить все зависимости из requirements.txt
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создать файл `.env` в папке `backend/` на основе шаблона `.env.example`:
```bash
# Скопировать шаблон (Linux/Mac)
cp .env.example .env

# Скопировать шаблон (Windows)
copy .env.example .env
```

**Отредактировать `.env` файл своими настройками:**

**Для разработки (SQLite):**
```env
# Django settings
SECRET_KEY=django-insecure-your-development-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite для разработки)
DB_ENGINE=django.db.backends.sqlite3

# CORS settings 
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Для production (PostgreSQL):**
```env
# Django settings
SECRET_KEY=your-production-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL для production)
DB_NAME=homebudget
DB_USER=homebudget_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# CORS settings
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 5. Применение миграций
```bash
# Создать все таблицы в базе данных
python manage.py migrate

# Загрузить начальные данные (категории)
python manage.py loaddata categories

# Создать суперпользователя для админ-панели
python manage.py createsuperuser
```

### 6. Запуск сервера разработки
```bash
# Запустить development сервер
python manage.py runserver
```

**Backend будет доступен по адресу:** http://localhost:8000

**Админ-панель:** http://localhost:8000/admin

---

##  Code Style Guide

Команда следует единым правилам написания кода согласно **Code Style Guide**:

### Общие правила Python

-  **PEP8** — стандарт оформления кода Python
-  **flake8** / **black** — автоматическая проверка и форматирование
-  **4 пробела** — для отступов (не табуляция!)
-  **79 символов** — максимальная длина строки
-  **Комментарии на русском языке**

### Именование

| Тип | Стиль | Пример |
|-----|-------|--------|
| Переменные и функции | `snake_case` | `user_balance`, `get_transactions()` |
| Классы | `PascalCase` | `User`, `BudgetViewSet` |
| Константы | `UPPER_CASE` | `MAX_UPLOAD_SIZE`, `DEFAULT_CURRENCY` |

### Документация кода

**Обязательные docstrings для:**
- Всех классов (модели, ViewSets, Serializers)
- Всех функций и методов
- Всех модулей (файлов)

**Формат docstring:**
```python
def get_user_balance(user_id):
    """
    Получить текущий баланс пользователя.
    
    Args:
        user_id (int): ID пользователя
    
    Returns:
        Decimal: текущий баланс
    
    Raises:
        User.DoesNotExist: если пользователь не найден
    """
    pass
```

### Git Flow

**Ветки именуются по шаблону:**
- `feature/название-фичи` — новая функциональность
- `bugfix/описание-бага` — исправление ошибок
- `hotfix/критическое-исправление` — срочные исправления в production
- `refactor/улучшения` — рефакторинг без изменения функционала
- `docs/документация` — изменения в документации

**Коммиты оформляются по Conventional Commits:**
- `feat: добавить endpoint для транзакций` — новая функциональность
- `fix: исправить расчёт баланса` — исправление бага
- `docs: обновить README` — изменения в документации
- `refactor: оптимизировать запросы к БД` — рефакторинг кода
- `style: исправить форматирование` — исправления стиля (без изменения логики)
- `chore: обновить зависимости` — технические изменения

**Перед коммитом обязательно:**
1. Запустить линтер: `flake8`
2. Запустить тесты: `python manage.py test`
3. Проверить что всё работает

---

## Тестирование
```bash
# Запустить все тесты
python manage.py test

# Запустить тесты конкретного приложения
python manage.py test apps.users

# Запустить тесты с verbose output
python manage.py test --verbosity=2

# Запустить конкретный тест
python manage.py test apps.users.tests.test_models.UserModelTest
```

---

## Полезные команды
```bash
# Создать новую миграцию
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить интерактивную консоль Django
python manage.py shell

# Собрать статические файлы (для production)
python manage.py collectstatic

# Проверить проект на ошибки
python manage.py check
```

---

## API Endpoints

После запуска сервера API будет доступно по адресу: `http://localhost:8000/api/`

**Документация API:** (будет добавлена позже)

**Основные endpoints:**
- `POST /api/token/` — получить JWT токен (login)
- `POST /api/token/refresh/` — обновить JWT токен
- `GET /api/users/profile/` — получить профиль пользователя
- `GET /api/budgets/` — список бюджетов
- `GET /api/transactions/` — список транзакций
- `GET /api/categories/` — список категорий

---
