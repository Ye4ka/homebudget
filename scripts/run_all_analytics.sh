#!/bin/bash
echo "Запуск аналитических отчетов..."
echo "1. Баланс за период"
psql $DATABASE_URL -f sql/analytics/01_balance_period.sql
echo "2. Топ категорий"
psql $DATABASE_URL -f sql/analytics/02_top_categories.sql
echo "3. Дневная динамика"
psql $DATABASE_URL -f sql/analytics/03_daily_dynamics.sql
echo "4. Месячное сравнение"
psql $DATABASE_URL -f sql/analytics/04_monthly_comparison.sql
