

from schemas.post import PostRequest
from core.config import settings
from core.api import RestAPI
from fastapi import HTTPException
import logging

logger = logging.getLogger("app")


async def get_image_binary(post_image):
    response = await RestAPI().send_request(method="get", url=post_image)
    if response.status_code not in [200, 201]:
        logger.error(
            f"Failed to fetch image. Status code: {response.status_code}")
        return None

    return response.content


async def get_linkedin_upload_link(access_token):
    url = f"{settings.LINKEDIN_API_BASE_URL}/assets?action=registerUpload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "registerUploadRequest": {
            "owner": f"urn:li:organization:{settings.LINKEDIN_ORGANIZATION_ID}",
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "serviceRelationships": [
                {
                    "identifier": "urn:li:userGeneratedContent",
                    "relationshipType": "OWNER"
                }
            ],
            "supportedUploadMechanism": ["SYNCHRONOUS_UPLOAD"]
        }
    }
    response = await RestAPI().send_request("post", url, json=data, headers=headers)
    if response.status_code not in [200, 201]:
        raise f"Request Failed. Status Code: {response.status_code}, Error: {response.text}"
    return response.json()


async def put_image_to_linkedin(url, image_data, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "image/png",
    }
    response = await RestAPI().send_request("post", url=url, content_type="form", data=image_data, headers=headers)
    if response.status_code not in [200, 201]:
        raise f"Request Failed. Status Code: {response.status_code}, Error: {response.text}"
    return response


async def publish_linkedin_post(post: PostRequest, access_token: str):
    image_data = None
    media = None

    if post.image:
        image_data = await get_image_binary(post.image)

    if image_data:
        response = await get_linkedin_upload_link(access_token)
        url = response.get("value", {}).get("uploadMechanism", {}).get(
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {}).get("uploadUrl")
        asset = response.get("value", {}).get("asset")
        response = await put_image_to_linkedin(url, image_data, access_token)
        media = [
            {
                "status": "READY",
                "description": {
                    "text": post.subtitle
                },
                "media": asset,
                "title": {
                    "text": post.title
                }
            }
        ]

    url = f"{settings.LINKEDIN_API_BASE_URL}/ugcPosts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "author": f"urn:li:organization:{settings.LINKEDIN_ORGANIZATION_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post.content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    if media:
        data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
        data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = media

    response = await RestAPI().send_request("post", url, json=data, headers=headers)
    if response.status_code not in [200, 201]:
        raise f"Request Failed. Status Code: {response.status_code}, Error: {response.text}"
    return response.json()
