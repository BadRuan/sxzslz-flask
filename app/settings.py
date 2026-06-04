from os import path, getcwd
from typing import Set
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/dbname"
    DB_ECHO: bool = False
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-in-production"
    UPLOAD_FOLDER: str = path.join(getcwd(), 'uploads')
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024 # 最大16MB
    ALLOWED_EXTENSIONS: Set[str] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding= 'utf-8',
        extra = "ignore"
        )

settings: Settings = Settings()