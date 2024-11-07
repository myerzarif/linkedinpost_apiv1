from pydantic import BaseModel
from typing import Optional


class TokenRequest(BaseModel):
    state: Optional[str] = None
    code: Optional[str] = None
