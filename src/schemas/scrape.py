
from pydantic import BaseModel
from typing import Optional


class ScrapeRequest(BaseModel):
    base_url: Optional[str] = None
    max_depth: Optional[int] = None
