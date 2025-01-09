from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models import PydanticObjectId


class TokenRequest(BaseModel):
    state: Optional[str] = None
    code: Optional[str] = None


class TokenResponse(BaseModel):
    id: PydanticObjectId
    token: str = None
    exp: datetime = None
    created: datetime = None

    class Config:
        orm_mode = True


class LinkedinToken(BaseModel):
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    refresh_token_expires_in: Optional[int] = None
    scope: Optional[str] = None
    token_type: Optional[str] = None
    id_token: Optional[str] = None


class ImageRequest(BaseModel):
    post_id: str
    note: Optional[str] = None
