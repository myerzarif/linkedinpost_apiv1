from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
import logging
from models.post import Post
from models.page import Page
from models.auth import AccessToken

logger = logging.getLogger("app")


async def init_mongodb():
    """Initialize MongoDB connection and Beanie ODM"""
    try:
        connection_string = settings.MONGO_CONNECTION_STRING
        client = AsyncIOMotorClient(connection_string, tz_aware=True)
        await init_beanie(
            database=getattr(client, settings.MONGO_DATABASE),
            document_models=[Post, Page, AccessToken],
        )

        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
