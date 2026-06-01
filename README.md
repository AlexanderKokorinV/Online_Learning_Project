# Online Learning Project

## Описание

Проект Online Learning Project представляет собой бэкенд-приложение для системы онлайн-обучения с кастомной авторизацией по Email и полноценным REST API для управления курсами и уроками.

## Технологии

*   **Backend:** Python / Django / Django REST Framework (DRF)
*   **Database:** PostgreSQL (хранение данных и истории отправок)
*   **Dependencies:** Poetry (управление пакетами и виртуальным окружением)

## Основные эндпоинты API (Маршруты)

### Пользователи (`/users/`)
* `GET /users/profile/<id>/` — Просмотр профиля пользователя.
* `PATCH /users/profile/<id>/` — Частичное редактирование профиля (город, телефон, аватар).

### Курсы и Уроки (`/learnings/`)
* `GET /learnings/courses/` — Получить список всех курсов (с вложенными уроками).
* `POST /learnings/courses/` — Создать новый курс.
* `GET /learnings/lessons/` — Получить список всех уроков.
* `POST /learnings/lessons/create/` — Создать новый урок (требуется передать `course` id).
* `PATCH /learnings/lessons/update/<id>/` — Редактировать урок.
* `DELETE /learnings/lessons/delete/<id>/` — Удалить урок.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/AlexanderKokorinV/Online_Learning_Project.git
```
2. Установите зависимости:
```
poetry config virtualenvs.in-project true --local
poetry install
```
3. Конфигурация переменных окружения
Создайте в корневом каталоге файл **`.env`** и заполните его по образцу:
```
# Создайте файл .env из копии этого файла и замените значения переменных реальными данными
SECRET_KEY=my_SECRET_KEY #Ваш_SECRET_KEY
DEBUG=True

# Конфигурация базы данных
DB_NAME=my_data_base # Имя базы данных
DB_USER=username # Имя пользователя (например, postgres)
DB_PASSWORD=password # Пароль базы данных
DB_HOST=localhost # Хост для базы данных
DB_PORT=5432 # Номер порта, который закреплен за PostgreSQL по умолчанию
```

4. Подготовка базы данных и миграции:

Перед запуском проекта убедитесь, что на вашем компьютере установлена и запущена СУБД **PostgreSQL**.
Создайте пустую базу данных, например, online_learning.

Выполните миграции Django для создания таблиц:
```
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

5. Создание суперпользователя (Администратора)

Создайте аккаунт администратора для доступа в панель управления. В качестве логина система запросит **Email**:
```
poetry run python manage.py createsuperuser
```

6. Запуск сервера разработки
```
poetry run python manage.py runserver
```

## Тестирование

Все эндпоинты успешно протестированы через **Postman**. Запросы выполняются без авторизации (на текущем этапе разработки).
## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).