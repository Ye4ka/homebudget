# Конфигурация Базы Данных HomeBudget

##  Подключение к Базе Данных

### Параметры подключения
- **Хост:** `localhost`
- **Порт:** `5432`
- **База данных:** `homebudget`
- **Пользователь:** `myuser`
- **Строка подключения:** `postgres://myuser:********@localhost:5432/homebudget`

### Для Django (.env файл)
```ini
DATABASE_URL=postgres://myuser:password@localhost:5432/homebudget