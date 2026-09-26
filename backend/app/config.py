"""Application configuration via environment variables."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "real-estate-lead-bot"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    API_PREFIX: str = "/api"

    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # MySQL (local development)
    DATABASE_URL: str = "mysql+aiomysql://root:password@localhost:3306/leadbot"
    DATABASE_URL_SYNC: str = "mysql+pymysql://root:password@localhost:3306/leadbot"

    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    N8N_WEBHOOK_SECRET: str = "change-me"
    N8N_BASE_URL: str = "http://localhost:5678"

    AI_API_KEY: str = ""
    AI_MODEL: str = "gpt-4o-mini"
    AI_BASE_URL: str = "https://api.openai.com/v1"
    AI_TIMEOUT_SECONDS: int = 30
    AI_MAX_RETRIES: int = 2

    FRONTEND_URL: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
