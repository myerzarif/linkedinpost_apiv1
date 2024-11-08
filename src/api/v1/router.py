from fastapi import APIRouter
from api.v1.endpoints import user
from api.v1.endpoints import auth
from api.v1.endpoints import post

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(post.router, prefix="/post", tags=["post"])