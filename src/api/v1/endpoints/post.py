from fastapi import APIRouter, Depends
from typing import List
from models.auth import AccessToken
from core.auth import validate_token
from schemas.post import PostRequest
from services.linkedin import publish_linkedin_post
router = APIRouter()

# publish post to linkedin
@router.post("/linkedin")
async def publish_linkedin(payload: PostRequest, access_token: AccessToken = Depends(validate_token)):
    response = await publish_linkedin_post(payload, access_token.token)
    return "Post Published Successfully!"
