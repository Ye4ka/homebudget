// Форматирование валюты
export function formatCurrency(value, locale = 'ru-RU', currency = 'RUB') {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
  }).format(value);
}

// Форматирование даты
export function formatDate(date, locale = 'ru-RU') {
  return new Intl.DateTimeFormat(locale).format(new Date(date));
}
