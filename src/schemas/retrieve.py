from pydantic import BaseModel
from typing import Optional
from pydantic.fields import Field
from models import PydanticObjectId


class RetrieveRequest(BaseModel):
    number_of_posts: Optional[int] = Field(
        default=5, ge=1, le=20, description="Number of posts to retrieve (1-20)")
    extra_prompt: Optional[str] = None


class RegeneratePostRequest(BaseModel):
    post_id: PydanticObjectId
    post_content: str
    extra_prompt: str
