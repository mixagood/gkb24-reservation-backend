# Сервис на FastApi по бронированию переговорных комнат

## Для чего

... - скоро дополню

## Используемые технологии

- FastApi = асинхронный веб-фреймворк для создания API
- SQLAlchemy = ORM для работы с РСУБД
- Alembic = для миграций БД
- Pydantic = валидация данных с использованией тайп-хитингов
- Aiosqlite = асинхронный интерфейс для SQLite
- Uvicorn = ASGI веб-сервер

## Подготовка к запуску

В корневой директории создайте файл `.env` и пропишите там настройки для отображаемого названия приложения и драйвер БД с директорией к файлу БД:

```text
APP_TITLE=Сервис бронирования переговорных комнат
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
```

Создайте виртуальное окружение командой:

```bash
python -m venv venv
```

И выполните установку всех зависимостей проекта:

```bash
pip install -m requirements.txt
```

Когда установка зависимостей завершиться, можно запускать проект, но перед этим необходимо произвести миграции в БД:

```bash
alembic upgrade head
```

## Работа с проектом

Запускаем проект:

```bash
uvicorn app.main:app
```

... - скоро дополню
