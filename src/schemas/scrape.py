
from pydantic import BaseModel
from typing import Optional


class ScrapeRequest(BaseModel):
    base_url: Optional[str] = None
    max_depth: Optional[int] = 2


class PageResponse(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    keywords: Optional[str] = None
    content: str

    class Config:
        orm_mode = True


class ScrapeResponse(BaseModel):
    message: str
