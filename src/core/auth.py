from schemas.auth import TokenRequest
from core.api import RestAPI
from core.config import settings
from models.auth import AccessToken
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends, status, Request
from typing import Optional
from datetime import datetime, timezone
from models.enums import HttpMethod, HttpContentType

async def get_linkedin_token(request: TokenRequest):
    data = {
        "grant_type": "authorization_code",
        "code": request.code,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URL,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_SECRET_ID
    }
    response = await RestAPI().send_request(method=HttpMethod.POST,
                                            url=settings.LINKEDIN_TOKEN_URL,
                                            content_type=HttpContentType.FORM,
                                            data=data,
                                            headers={"Content-Type": "application/x-www-form-urlencoded"})
    return response.json()


async def initiate_token(request: TokenRequest):
    linkedin_response = await get_linkedin_token(request)
    token = await AccessToken.create_token(linkedin_response)
    return token


# Custom scheme to extract the token
class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme.",
            )
        return credentials


token_scheme = TokenBearer()


async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(token_scheme)):
    token_str = credentials.credentials  # Extract the actual token value

    # Find the token in the database
    access_token = await AccessToken.find_one(AccessToken.token == token_str)

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found.",
        )

    # Check if the token has expired
    if access_token.exp and access_token.exp < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired.",
        )

    return access_token
