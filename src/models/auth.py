from datetime import datetime, timedelta, timezone
from typing import Optional
from core.config import settings
from schemas.auth import LinkedinToken
from models import BaseDocument


class AccessToken(BaseDocument):
    token: str = None
    exp: datetime = None
    linkedin_token: Optional[LinkedinToken] = None

    class Settings:
        name = "access_tokens"
        use_state_management = True

    @classmethod
    async def create_token(cls, linkedin_token: LinkedinToken) -> "AccessToken":
        token = linkedin_token.get("access_token")
        expiry_date = datetime.now(
            timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME)
        access_token = cls(token=token, exp=expiry_date,
                           linkedin_token=linkedin_token)
        await access_token.insert()
        return access_token
