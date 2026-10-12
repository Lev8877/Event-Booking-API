# Event Booking API

Данное приложение представляет собой REST API для управления мероприятиями и бронирования мест. Пользователи могут регистрироваться, просматривать мероприятия и бронировать места. Администратор может создавать, изменять и удалять мероприятия.

Проект реализован на FastAPI и PostgreSQL. Для работы с базой данных используется асинхронный SQLAlchemy, для миграций Alembic. Приложение можно запустить локально или через Docker Compose.

## Стек

Python 3.13  
FastAPI, Pydantic  
PostgreSQL  
SQLAlchemy, asyncpg  
Alembic  
JWT, OAuth2  
pwdlib, Argon2  
Pytest, TestClient  
Docker, Docker Compose

## Возможности

Регистрация и авторизация пользователей  
Проверка уникальности username и email  
Access и refresh токены, хранение refresh токена в HttpOnly cookie  
Обновление токена и выход из аккаунта  
Роли user и admin  
Создание, изменение и удаление мероприятий администратором  
Поиск, фильтрация и пагинация списка мероприятий  
Создание, просмотр и удаление своих бронирований  
Каскадное удаление бронирований при удалении мероприятия

### Правила бронирования

Нельзя бронировать прошедшие мероприятия  
Нельзя дважды забронировать одно мероприятие  
Количество бронирований не может превышать максимальное число участников  
Пользователь не может удалить чужую бронь

## Структура проекта

```text
alembic/          Миграции базы данных
models/           Модели SQLAlchemy
routers/          Маршруты API
schemes/          Схемы Pydantic
security/         JWT
services/         Бизнес-логика
tests/            Тесты
main.py           Точка входа в приложение
database.py       Базовый класс моделей
dependencies.py   Зависимости FastAPI
Dockerfile        Сборка образа
compose.yaml      Настройка Docker Compose
requirements.txt  Зависимости Python
```

## Настройка .env

Создайте файл .env в корне проекта. За основу можно взять .env.example. Укажите параметры своей базы данных, секретный ключ и настройки PostgreSQL для Docker Compose.

Экземпляр:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:change_me@localhost:5432/Event%20Booking%20API
TEST_DATABASE_URL=postgresql+asyncpg://postgres:change_me@localhost:5432/event_booking_test
SECRET_KEY=replace_with_random_secret
ALGORITHM=your_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=58
REFRESH_TOKEN_EXPIRE_DAYS=58

POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me
POSTGRES_DB=Event Booking API
```

Для локального запуска укажите адрес своей PostgreSQL в DATABASE_URL. Для тестов используйте отдельную базу данных в TEST_DATABASE_URL.

Название основной базы содержит пробелы, поэтому в URL используется %20.

Файл .env не должен попадать в Git.

## Запуск через Docker Compose

Для запуска необходим Docker с поддержкой Compose.

```bash
docker compose up --build
```

При запуске создаются контейнеры FastAPI и PostgreSQL. Миграции Alembic применяются автоматически.

Swagger: http://localhost:8000/docs

Остановить и удалить контейнеры:

```bash
docker compose down
```

Данные PostgreSQL сохраняются в Docker Volume. Команда docker compose down -v удаляет том с данными.

## Локальный запуск

Установите Python 3.13 и PostgreSQL, создайте базу данных и настройте .env.

Создать виртуальное окружение и установить зависимости:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Применить миграции:

```powershell
py -m alembic upgrade head
```

Запустить приложение:

```powershell
uvicorn main:app --reload
```

Swagger: http://localhost:8000/docs

## Тесты

Для тестов нужна отдельная база PostgreSQL, указанная в TEST_DATABASE_URL. Базу необходимо создать до запуска тестов.

```powershell
py -m pytest -v
```

Тесты используют TestClient и отдельную тестовую базу. Данные в ней очищаются перед каждым тестом и после него.

Реализованы проверки регистрации, авторизации, доступа к маршрутам и части ошибок при работе с мероприятиями и бронированиями.

## Основные маршруты

POST /register: Регистрация  
POST /login: Вход  
GET /me: Данные пользователя  
POST /refresh: Обновление access токена  
POST /logout: Выход  
GET /events: Список мероприятий  
GET /events/{event_id}: Получение мероприятия  
POST /events: Создание мероприятия (admin)  
PATCH /events/{event_id}: Изменение мероприятия (admin)  
DELETE /events/{event_id}: Удаление мероприятия (admin)  
POST /events/{event_id}/bookings: Бронирование места  
GET /bookings: Список своих бронирований  
DELETE /bookings/{booking_id}: Удаление своей брони

Для защищённых маршрутов используется JWT в заголовке Authorization: Bearer. Маршрут /login принимает username и password как данные формы.

## Коды ответов

200: успешный запрос  
401: ошибка аутентификации  
403: недостаточно прав  
404: ресурс не найден  
409: конфликт, например повторная бронь или отсутствие свободных мест  
422: некорректные данные запроса