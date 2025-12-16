# СИСТЕМА РЕЗЕРВНОГО КОПИРОВАНИЯ И ВОССТАНОВЛЕНИЯ

## ОБЗОР

Данный документ описывает процедуры резервного копирования и восстановления базы данных HomeBudget. Система обеспечивает:
- Ежедневное автоматическое резервное копирование
- Ротацию резервных копий (7 дней)
- Проверку целостности архивов
- Процедуру восстановления с проверками

## СТРУКТУРА ФАЙЛОВ
homebudget/
├── scripts/
│ ├── backup.sh # Основной скрипт backup
│ ├── restore.sh # Скрипт восстановления
│ ├── backup_config.env # Конфигурация
│ └── test_backup_restore.sh # Тестовый скрипт
├── docs/database/
│ └── backup-recovery.md # Эта документация
└── /var/
├── backups/homebudget/ # Директория с бэкапами
└── log/homebudget/ # Логи backup/restore

text

## КОНФИГУРАЦИЯ

### Настройка параметров
Отредактируйте файл `backup_config.env`:

```bash
# Основные параметры
DB_NAME="homebudget"
DB_USER="myuser"
DB_HOST="localhost"

# Директории
BACKUP_DIR="/var/backups/homebudget"
LOG_DIR="/var/log/homebudget"

# Ротация
RETENTION_DAYS=7
MAX_BACKUPS=10
Создание директорий
bash
sudo mkdir -p /var/backups/homebudget
sudo mkdir -p /var/log/homebudget
sudo chown -R postgres:postgres /var/backups/homebudget
sudo chown -R postgres:postgres /var/log/homebudget
🚀 ИСПОЛЬЗОВАНИЕ
Ручное создание резервной копии
bash
