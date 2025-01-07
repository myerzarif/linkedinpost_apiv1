from pydantic_settings import BaseSettings
from models.enums import EnvEnum


class Settings(BaseSettings):
    ENV: str = "DEV"
    PROJECT_NAME: str = "Linkedin Content Generation"
    API_STR: str = "/api"
    SECRET_KEY: str = '59TpzL9Cvjft0_CYsBFMkwIqxME0Ey59vxN0Ow9a1Vc'
    TIMEOUT: int = 5
    DB_URL: str = ""
    LOG_PATH: str = "log/app.log"
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

    COHERE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    NVIDIA_API_KEY: str = ""
    NVIDIA_BASIC_AUTH: str = ""

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

    class Config:
        env_file = ".env"


settings = Settings()
