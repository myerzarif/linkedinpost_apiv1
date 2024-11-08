
from datetime import datetime
from typing import Optional
from pydantic.fields import Field
from beanie import Document


class Post(Document):
    title: Optional[str] = None
    author: Optional[str] = None
    subtitle: Optional[str] = None
    image: Optional[str] = None
    content: str
    created: datetime = Field(default_factory=datetime.now)

    @classmethod
    async def get_by_title(cls, *, title: str) -> Optional["Post"]:
        return await cls.find_one(cls.title == title)

    @classmethod
    async def get_top(cls, *, offset: int = 0, limit: int = 50) -> Optional["Post"]:
        return await cls.find({}).sort(-cls.created).skip(offset).limit(limit).to_list()
        # return cls.find_many()

    @classmethod
    async def bulk_insert(cls, items: any) -> Optional["Post"]:
        posts = [Post(
            title=item.get("title", ""),
            subtitle=item.get("subtitle", ""),
            content=item.get("content", ""),
        ) for item in items]
        return await cls.insert_many(posts)

    class Settings:
        name = "posts"
        use_state_management = True
