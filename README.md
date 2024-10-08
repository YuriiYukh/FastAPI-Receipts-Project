# FastAPI Receipts Project

Цей проект створює REST API для керування чеками продажу, включаючи реєстрацію користувачів, авторизацію та перегляд чеків у текстовому форматі. Проект використовує FastAPI та PostgreSQL для зберігання даних.

## Вимоги

- Python 3.8+
- PostgreSQL
- Пакетний менеджер `pip`
- Віртуальне середовище (рекомендовано для ізоляції залежностей)

## Налаштування

1. Клонування репозиторію

   ```
   git clone https://your-repo-url.git
   cd project-root
   ```

2. Створення віртуального середовища

   ```
   python -m venv venv
   source venv/bin/activate  # Unix/MacOS
   .\venv\Scripts\activate  # Windows
   ```

3. Встановлення залежностей

   ```
   pip install -r requirements.txt
   ```

4. Налаштування бд. Переконайтеся, що постгрес запущений і створіть базу даних:

   ```
   CREATE DATABASE fastapi_receipts_db;
   ```

5. Створіть .env файл, відповідно до змінних в .env.example

## Запуск проекту

Запуск проекту локально за допомогою Uvicorn з раніше встановленого venv:

    ```
    uvicorn main:app --reload
    ```

Згенерована документація з описом ендпоінтів доступна за посиланням /docs.
