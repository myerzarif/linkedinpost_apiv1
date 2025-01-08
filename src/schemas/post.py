from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from pydantic.fields import Field
from models import PydanticObjectId


class PostResponse(BaseModel):
    id: PydanticObjectId
    title: Optional[str] = None
    author: Optional[str] = None
    subtitle: Optional[str] = None
    image: Optional[str] = None
    content: str
    published: bool = False
    post_statistics: Optional[Dict] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class PostRequest(BaseModel):
    id: PydanticObjectId
    title: Optional[str] = None
    author: Optional[str] = None
    subtitle: Optional[str] = None
    image: Optional[str] = None
    content: str

    class Config:
        orm_mode = True
