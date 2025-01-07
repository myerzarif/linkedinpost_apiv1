from fastapi import APIRouter, Depends
from typing import List
from models.auth import AccessToken
from models.post import Post
from core.auth import validate_token
from schemas.post import PostRequest, PostResponse
from services.linkedin import publish_linkedin_post
from services.linkedin import linkedin_organization_statistics
from services.linkedin import linkedin_post_statistics

router = APIRouter()


@router.get("/", response_model=List[PostResponse])
async def get_posts(access_token: AccessToken = Depends(validate_token)):
    posts = await Post.get_top(offset=0, limit=100)
    for post in posts:
        if post.published and post.linkedin_id:
            post.post_statistics = await linkedin_post_statistics(access_token.token, post.linkedin_id)
    return posts


@router.get("/{id}", response_model=PostResponse)
async def get_post(id: str, access_token: AccessToken = Depends(validate_token)):
    post = await Post.get(id)
    return post


@router.post("/linkedin")
async def publish_linkedin(payload: PostRequest, access_token: AccessToken = Depends(validate_token)):
    response = await publish_linkedin_post(payload, access_token.token)
    return {"result": "Post Published Successfully!"}


@router.post("/linkedin/statistics/organization")
async def linkedin_statistics_organization(access_token: AccessToken = Depends(validate_token)):
    response = await linkedin_organization_statistics(access_token.token)
    return response
