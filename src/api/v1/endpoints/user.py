from fastapi import APIRouter
from models.user import User
from typing import List

router = APIRouter()


@router.get("/", response_model=List[User])
async def get_users():
    users = await User.find_all().to_list()
    return users


# @router.get("/{user_id}")
# async def get_user(user_id: str):
#     user = await User.get(user_id)
#     return [1, 2, 3]
