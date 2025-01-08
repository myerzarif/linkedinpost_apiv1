from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from fastapi import APIRouter, Depends
from models.post import Post
from schemas.auth import ImageRequest
from core.auth import validate_token
from models.auth import AccessToken

router = APIRouter()


@router.post("/")
async def create_image(payload: ImageRequest, access_token: AccessToken = Depends(validate_token)):
    post = await Post.get(payload.post_id)
    text_prompt = f"gnerate an image bease on the following info and make sure you are not adding text to image: title:{post.title}, note:{payload.note}"
    print("text_prompt[:1000]", text_prompt[:1000])
    image_url = DallEAPIWrapper(model="dall-e-3").run(text_prompt[:1000])
    await post.set({"image": image_url})
    return image_url
