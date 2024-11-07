from fastapi import APIRouter
from api.v1.endpoints import users
from api.v1.endpoints import auth

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])