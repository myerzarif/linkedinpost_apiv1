from fastapi import APIRouter
from api.v1.endpoints import auth
from api.v1.endpoints import post
from api.v1.endpoints import scrape
from api.v1.endpoints import image

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(post.router, prefix="/post", tags=["post"])
api_router.include_router(scrape.router, prefix="/scrape", tags=["scrape"])
api_router.include_router(image.router, prefix="/image", tags=["image"])
