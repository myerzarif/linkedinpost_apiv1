from fastapi import FastAPI
from core.config import settings
from api.v1.router import api_router as api_router_v1
from middleware.logging import setup_logging
from db.mongodb import init_mongodb
import logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from models.enums import EnvEnum
from core.config import settings


# Setup logging
setup_logging(log_level=settings.LOG_LEVEL)
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongodb()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,  # Allows cookies to be sent with requests
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router_v1, prefix=settings.API_V1_STR)

if settings.ENV == EnvEnum.PRODUCTION.value:
    app.openapi_url = ""


@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME}: Service is up and running.."}
