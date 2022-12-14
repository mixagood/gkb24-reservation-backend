# app/core/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "..."
    app_description: str = "..."
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    app_version: str = "1.0.5"

    class Config:
        env_file = ".env"


settings = Settings()
