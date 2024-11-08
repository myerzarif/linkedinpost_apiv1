from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic.fields import Field
from models import PydanticObjectId


class PostResponse(BaseModel):
    id: PydanticObjectId
    title: Optional[str] = None
    author: Optional[str] = None
    subtitle: Optional[str] = None
    image: Optional[str] = None
    content: str
    created: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class PostRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    subtitle: Optional[str] = None
    image: Optional[str] = None
    content: str

    class Config:
        orm_mode = True
