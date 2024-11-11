
from bson import ObjectId
from beanie import Document
from datetime import datetime, timezone
from typing import Optional


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, *args, **kwargs):
        return {"type": "string", "format": "objectid"}


class BaseDocument(Document):
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = None

    class Settings:
        use_revision = True  # Enable document revision tracking

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return await super().save(*args, **kwargs)