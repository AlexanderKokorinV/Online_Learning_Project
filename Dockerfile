# 1. Используем базовый образ Python 3.14 (slim-версия)
FROM python:3.14.0-slim

# 2. Настройки системного окружения Python и Poetry
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

# 3. Рабочая директория внутри контейнера
WORKDIR /app

# 4. Установка Poetry последней версии
RUN pip install --no-cache-dir poetry

# 5. Копирование конфигурационных файлов зависимостей
COPY pyproject.toml poetry.lock* ./

# 6. Установка только основных зависимостей проекта через pip
RUN poetry install --only main --no-root

# 7. Копирование исходного кода приложения Django
COPY . .

# 8. Открытие сетевого порта и команда старта
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]