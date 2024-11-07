from schemas.auth import TokenRequest
from api import RestAPI
from core.config import settings

async def get_linkedin_token(request: TokenRequest):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": request.code,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URL,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_SECRET_ID
    }
    response = await RestAPI().send_request(method="post", url=settings.LINKEDIN_TOKEN_URL, content_type="form", data=data, headers=headers)
    return response.json()