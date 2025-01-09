from fastapi import APIRouter, Depends
from schemas.auth import TokenRequest, TokenResponse
from urllib.parse import urlencode
from core.config import settings
from core.utils import random_number
from core.auth import initiate_token
from models.auth import AccessToken
from core.auth import validate_token

router = APIRouter()


@router.get("/authorization")
async def authorization():
    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URL,
        "state": str(random_number()),
        "scope": " ".join(settings.LINKEDIN_SCOPE)
    }
    response = {
        "redirect_url": f"{settings.LINKEDIN_AUTHORIZATION_URL}?{urlencode(params)}"
    }
    return response


@router.post("/token", response_model=TokenResponse)
async def get_token(data: TokenRequest):
    response = await initiate_token(data)
    return response


@router.post("/logout")
async def logout(access_token: AccessToken = Depends(validate_token)):
    await access_token.delete()
    return {"message": "Success"}
