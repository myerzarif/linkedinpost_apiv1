from datetime import datetime
from beanie import Document, Indexed
from typing import Optional, List
from pydantic.fields import Field


class Page(Document):
    url: Optional[str] = None
    title: Optional[str] = None
    keywords: Optional[str] = None
    content: str
    created: datetime = Field(default_factory=datetime.now)

    @classmethod
    async def get_by_url(cls, *, url: str) -> Optional["Page"]:
        return await cls.find_one(cls.url == url)

    @classmethod
    async def fetch_documents(cls, limit: int = 100) -> List["Page"]:
        documents = await cls.find().to_list(limit)
        return documents

    class Settings:
        name = "pages"
        use_state_management = True
