from fastapi import FastAPI
from core.config import settings
from api.v1.router import api_router as api_router_v1
from middleware.logging import setup_logging
from db.mongodb import init_mongodb
# from middleware.error_handler import APIErrorHandler
import logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from models import EnvEnum
from middleware.log_handler import LogRequestsMiddleware

# Setup logging
setup_logging(log_level=settings.LOG_LEVEL)
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongodb()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# Store settings in app state for access in middleware
app.state.settings = settings

# Add error handling middleware
# app.middleware("http")(APIErrorHandler())
app.add_middleware(LogRequestsMiddleware)
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
