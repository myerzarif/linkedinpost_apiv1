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
    LOG_BASE_DIR: str = "logs"
    MAX_BODY_SIZE: int = 1000

    # linkedin
    LINKEDIN_AUTHORIZATION_URL: str = ""
    LINKEDIN_TOKEN_URL: str = ""
    LINKEDIN_PUBLISH_URL: str = ""
    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_SECRET_ID: str = ""
    LINKEDIN_REDIRECT_URL: str = ""
    LINKEDIN_ORGANIZATION_ID: str = ""
    LINKEDIN_SCOPE: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
