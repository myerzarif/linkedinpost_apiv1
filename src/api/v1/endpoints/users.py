from fastapi import APIRouter, HTTPException, status
from models.user import User
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger("app")


@router.get("/", response_model=List[User])
async def get_users():
    users = await User.find_all().to_list()
    return users


# @router.get("/{user_id}")
# async def get_user(user_id: str):
#     user = await User.get(user_id)
#     return [1, 2, 3]

