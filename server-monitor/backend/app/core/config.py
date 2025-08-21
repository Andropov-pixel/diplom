from pydantic_settings import BaseSettings
from pydantic import AnyUrl, validator
from typing import List, Optional
import secrets
import os


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Server Monitoring System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # API
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/server_monitor"
    MONGODB_URL: str = "mongodb://localhost:27017/server_monitor"

    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_WEBHOOK_URL: Optional[str] = None

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8001"]

    # Encryption
    ENCRYPTION_KEY: str = secrets.token_urlsafe(32)

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [item.strip() for item in v.split(",")]
        return v


settings = Settings()