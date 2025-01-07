from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.user import User
from models.page import Page
import logging

logger = logging.getLogger("app")


async def init_mongodb():
    """Initialize MongoDB connection and Beanie ODM"""
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)

        # Initialize Beanie with the document models
        await init_beanie(
            database=client[settings.MONGODB_DB_NAME],
            document_models=[
                User,
                Page
            ]
        )

        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
