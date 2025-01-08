from fastapi import APIRouter, Depends
from services.retrieve import retrive_title_and_generate_posts, regenerate_post_content
from core.auth import validate_token
from models.auth import AccessToken
from schemas.retrieve import RetrieveRequest, RegeneratePostRequest

router = APIRouter()


@router.post("/generate")
async def retrieve(payload: RetrieveRequest, access_token: AccessToken = Depends(validate_token)):
    items = await retrive_title_and_generate_posts(payload)
    return items


@router.post("/regenerate")
async def update_post_content(payload: RegeneratePostRequest, access_token: AccessToken = Depends(validate_token)):
    response = await regenerate_post_content(payload)
    return response
