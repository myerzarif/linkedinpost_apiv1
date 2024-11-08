from pydantic import BaseModel
from typing import Optional


class TokenRequest(BaseModel):
    state: Optional[str] = None
    code: Optional[str] = None


class LinkedinToken(BaseModel):
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None
    token_type: Optional[str] = None
    id_token: Optional[str] = None