from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
from schemas.scrape import ScrapeRequest
from core.api import RestAPI
from models.enums import HttpMethod


async def scrape_website(params: ScrapeRequest):
    visited_urls = set()

    async def crawl(url, depth):
        if depth > params.max_depth or url in visited_urls:
            return

        # async with httpx.AsyncClient() as client:
        html = (await RestAPI().send_request(url=url, method=HttpMethod.GET)).text
        if html:
            visited_urls.add(url)
            soup = BeautifulSoup(html, 'html.parser')

            # Find all links on the current page
            tasks = []  # Track tasks separately for each call
            for link in soup.find_all('a', href=True):
                full_url = urljoin(params.base_url, link['href'])

                # Ensure the link is within the same domain
                if full_url.startswith(params.base_url) and full_url not in visited_urls:
                    # Schedule the crawl with a separate depth counter for each link
                    tasks.append(crawl(full_url, depth + 1))

            # Introduce a delay between each batch of link crawls
            await asyncio.sleep(0.2)
            await asyncio.gather(*tasks)  # Execute all crawls in parallel

    await crawl(params.base_url, 0)
    return visited_urls
