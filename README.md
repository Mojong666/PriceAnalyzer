# PriceAnalyzer

## Описание
**PriceAnalyzer** — это инструмент для анализа цен на товары из CSV файлов. Программа ищет файлы с ценами в указанной директории, загружает данные и предоставляет удобный интерфейс для поиска товаров и сравнения цен. Результаты поиска могут быть экспортированы в HTML файл.

## Основные функции
- Загрузка и анализ данных о товарах из CSV файлов.
- Автоматическое определение разделителя в CSV файлах.
- Нормализация заголовков для поиска необходимых столбцов (название, цена, вес).
- Поиск товаров по имени с сортировкой по цене за килограмм.
- Экспорт результатов поиска в HTML файл.

## Использование
Укажите путь к директории с вашими CSV файлами в коде (вместо "Укажите путь к файлам CSV").

## Структура проекта
- project.py - основной скрипт для запуска программы (запуск в pycharm 'Shift + F10').
- output.html - файл, в который экспортируются результаты поиска (создается после выполнения поиска).
