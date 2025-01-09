from pydantic_settings import BaseSettings
from models.enums import EnvEnum


class Settings(BaseSettings):
    ENV: str = "DEV"
    PROJECT_NAME: str = "Linkedin Content Generation"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = '59TpzL9Cvjft0_CYsBFMkwIqxME0Ey59vxN0Ow9a1Vc'
    TIMEOUT: int = 5
    BASIC_AUTH_USER: str = "basicuser"
    BASIC_AUTH_PASS: str = "basicpass"
    ACCESS_TOKEN_LIFETIME: int = 24 * 60 * 60
    SOFT_TOKEN_LIFETIME: int = 120
    VERIFICATION_CODE_LIFETIME: int = 300
    EMAIL_SENDER: str = 'no-reply@camros.no'
    OTP_LENGTH: int = 5
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 5050
    API_ROOT: str = "http://localhost:5050"
    WEB_ROOT: str = "http://localhost:3000"
    UPLOAD_ROOT: str = "http://localhost:5050"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    VALID_FILE_TYPES: list = ['csv']
    UPLOAD_PATH: str = '/apiv1/uploads'
    ALLOWED_ORIGINS: list = ["http://localhost", "http://localhost:3000"]
    VERIFIED_USERS: list = []

    LOG_BASE_DIR: str = "logs"
    LOG_LEVEL: str = "DEBUG"
    MAX_BODY_SIZE: int = 1000

    OPENAI_API_KEY: str = ""

    MONGO_CONNECTION_STRING: str = ""
    MONGO_DATABASE: str = ""
    MONGO_PORT: int = 27017
    MONGO_DATABASE: str = ""
    MONGO_USERNAME: str = ""
    MONGO_PASSWORD: str = ""

    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_ENDPOINT: str = ""
    LANGCHAIN_PROJECT: str = ""

    VECTOR_INDEX_NAME: str = ""
    PINECONE_API_KEY: str = ""

    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_SECRET_ID: str = ""
    LINKEDIN_REDIRECT_URL: str = ""
    LINKEDIN_ORGANIZATION_ID: str = ""
    LINKEDIN_API_BASE_URL: str = ""
    LINKEDIN_SCOPE: list = []
    LINKEDIN_AUTHORIZATION_URL: str = ""
    LINKEDIN_TOKEN_URL: str = ""

    COMPANY_NAME: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
