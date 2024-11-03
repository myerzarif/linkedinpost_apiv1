from pydantic_settings import BaseSettings
from typing import Optional
from models.common import EnvEnum


class Settings(BaseSettings):
    PROJECT_NAME: str = "LinkedInPostGeneration"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI project for generating linkedin posts"
    API_V1_STR: str = "/api/v1"

    # DEBUG mode
    ENV: str = EnvEnum.PRODUCTION.value
    DEBUG: bool = False

    # API info
    API_HOST: str = "0.0.0.0"
    API_PORT: int

    # MongoDB settings
    MONGODB_URL: str
    MONGODB_DB_NAME: str

    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALLOWED_ORIGINS: list = ["http://localhost", "http://localhost:3000"]

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
