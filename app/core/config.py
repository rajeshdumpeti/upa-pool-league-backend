# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, Field
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "UPA Pool League API"
    APP_ENV: str = Field(default="dev", description="dev | test | prod")
    VERSION: str = "0.1.0"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # CORS
    CORS_ORIGINS: List[str] = Field(default=["*"])

    # Data stores
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/upa"
    REDIS_URL: str | None = None  # optional for now

    # Security
    JWT_SECRET: str = "change-me-in-prod"
    JWT_ISSUER: str = "upa-api"
    JWT_AUDIENCE: str = "upa-mobile"
    JWT_EXPIRES_MIN: int = 60 * 24  # 24h

    # Pydantic Settings config
    model_config = SettingsConfigDict(
        env_prefix="UPA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Singleton settings object
settings = Settings()
