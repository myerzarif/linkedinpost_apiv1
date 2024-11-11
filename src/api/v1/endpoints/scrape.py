from fastapi import APIRouter, Depends
from services.scrape import scrape_website
from core.auth import validate_token
from models.auth import AccessToken
from schemas.scrape import ScrapeRequest

router = APIRouter()

# 1. scrape the site (get each page url, get its content and save it to mongodb)
# 2. store web pages to a vector db
@router.post("/")
async def preprocessing(params: ScrapeRequest, access_token: AccessToken = Depends(validate_token)):
    all_pages = await scrape_website(params)
    return all_pages
