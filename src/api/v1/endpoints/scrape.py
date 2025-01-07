from fastapi import APIRouter, Depends
from services.scrape import scrape_website, save_pages_to_mongo, store_in_vector_db
from core.auth import validate_token
from models.auth import AccessToken
from schemas.scrape import ScrapeRequest, PageResponse, ScrapeResponse
from typing import List

router = APIRouter()


@router.post("/")
async def preprocessing(params: ScrapeRequest):
    all_pages = await scrape_website(params)
    inserted_links = await save_pages_to_mongo(all_pages)
    return inserted_links


@router.post("/vector/save", response_model=ScrapeResponse)
async def vector_save(access_token: AccessToken = Depends(validate_token)):
    await store_in_vector_db()
    return ScrapeResponse(
        message="embeddings saved in vector db successfully!"
    )
