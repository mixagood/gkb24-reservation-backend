# app/main.py
from fastapi import FastAPI
from app.core.config import settings

# Импортируем роутер
# и корутину для создания первого суперюзера
from app.api.routers import main_router
from app.core.init_db import create_first_superuser

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    redoc_url=None,
)

# Для работы фронта
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://127.0.0.1:5173",  # Vite Dev Server
    "http://127.0.0.1",  # Если запущено через Apache
]

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Источник запросов (фронтенд)
    allow_credentials=True,                   # Разрешение на отправку cookies
    allow_headers=["*"],                      # Разрешить все заголовки
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],  # Явное указание разрешенных методов
)


# Подключаем роутер
app.include_router(main_router)


@app.on_event("startup")
async def startup():
    await create_first_superuser()
