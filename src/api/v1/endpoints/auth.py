from fastapi import APIRouter, HTTPException, status, Depends
from models.user import User
from typing import List
import logging
from schemas.auth import TokenRequest
from urllib.parse import urlencode
from core.config import settings
from core.utils import random_number

router = APIRouter()
logger = logging.getLogger("app")


@router.get("/linkedin/authorization")
async def authorization():
    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URL,
        "state": random_number(),
        "scope": settings.LINKEDIN_SCOPE
    }
    return f"{settings.LINKEDIN_AUTHORIZATION_URL}?{urlencode(params)}"


@router.get("/linkedin/token")
async def get_token(request: TokenRequest = Depends()):
    
    return {"state": request.state, "code": request.code}
