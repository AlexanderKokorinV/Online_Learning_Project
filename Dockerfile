# 1. Используем базовый образ Python 3.14 (slim-версия)
FROM python:3.14.0-slim

# 2. Настройки системного окружения Python и Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=2.2.1 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH"

# 3. Рабочая директория внутри контейнера
WORKDIR /app

# 4. Установка системных утилит и Poetry
RUN apt-get update && apt-get install --no-install-recommends -y curl \
    && curl -sSL https://python-poetry.org | python3 - \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. Копирование конфигурационных файлов зависимостей
COPY pyproject.toml poetry.lock* ./

# 6. Установка только основных зависимостей проекта
RUN poetry install --no-root --only main

# 7. Копирование исходного кода приложения Django
COPY . .

# 8. Открытие сетевого порта и команда старта
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]