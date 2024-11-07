from beanie import Indexed
from pydantic import EmailStr
from models.common import BaseDocument
from typing import Optional
from typing import Annotated


class User(BaseDocument):
    email: Annotated[EmailStr, Indexed(unique=True)]

    class Settings:
        name = "users"  # Collection name in MongoDB