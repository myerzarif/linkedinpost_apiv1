from beanie import Document, Indexed
from datetime import datetime
from typing import Optional
from enum import Enum


class BaseDocument(Document):
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None

    class Settings:
        use_revision = True  # Enable document revision tracking

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return await super().save(*args, **kwargs)


class EnvEnum(Enum):
    DEV = "DEV"
    STAGE = "STAGE"
    PRODUCTION = "PRODUCTION"
