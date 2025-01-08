
from datetime import datetime
from typing import Optional, Dict
from pydantic.fields import Field
from models import BaseDocument


class Post(BaseDocument):
    title: Optional[str] = None
    author: Optional[str] = None
    subtitle: Optional[str] = None
    image: Optional[str] = None
    published: bool = False
    content: str
    linkedin_id: Optional[str] = None
    post_statistics: Optional[Dict] = None

    @classmethod
    async def get_by_title(cls, *, title: str) -> Optional["Post"]:
        return await cls.find_one(cls.title == title)

    @classmethod
    async def get_top(cls, *, offset: int = 0, limit: int = 50) -> Optional["Post"]:
        return await cls.find({}).sort(-cls.created_at).skip(offset).limit(limit).to_list()

    @classmethod
    async def bulk_insert(cls, items: any) -> Optional["Post"]:
        posts = [Post(
            title=item.get("title", ""),
            subtitle=item.get("subtitle", ""),
            content=item.get("content", ""),
        ) for item in items]
        return await cls.insert_many(posts)

    @classmethod
    async def update_post(cls, id, **kwargs) -> Optional["Post"]:
        if not id or not kwargs:
            return

        post = await Post.get(id)

        if not post:
            return

        await post.update({"$set": kwargs})

    class Settings:
        name = "posts"
        use_state_management = True
