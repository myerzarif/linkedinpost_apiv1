from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
from schemas.scrape import ScrapeRequest
from core.api import RestAPI
from models.enums import HttpMethod
from models.page import Page as WebPage
from bs4 import BeautifulSoup
from ai_models.model_factory import embedding as ai_embedding
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import uuid
from langchain_pinecone import PineconeVectorStore
from core.extension import pc
from core.config import settings


def get_page_model(soup, url) -> WebPage:
    if not soup:
        return None

    # Extract the title
    title = soup.title.string if soup.title else "No Title"

    # Extract meta keywords if available
    keywords_meta = soup.find("meta", attrs={"name": "keywords"})
    keywords = keywords_meta["content"] if keywords_meta else "No Keywords"

    # Extract all text content from the page
    content = soup.get_text(separator="\n")

    return WebPage(
        url=url,
        title=title,
        keywords=keywords,
        content=content
    )


async def scrape_website(params: ScrapeRequest):
    visited_urls = set()
    all_pages: list[WebPage] = []

    async def crawl(url, depth):
        if depth > params.max_depth or url in visited_urls:
            return

        # async with httpx.AsyncClient() as client:
        html = await RestAPI().send_request(url=url, method=HttpMethod.GET)
        html = html.text
        if html:
            visited_urls.add(url)
            soup = BeautifulSoup(html, 'html.parser')
            page_info = get_page_model(soup, url)
            all_pages.append(page_info)

            # Find all links on the current page
            tasks = []  # Track tasks separately for each call
            for link in soup.find_all('a', href=True):
                full_url = urljoin(params.base_url, link['href'])

                # Ensure the link is within the same domain
                if full_url.startswith(params.base_url) and full_url not in visited_urls:
                    # Schedule the crawl with a separate depth counter for each link
                    tasks.append(crawl(full_url, depth + 1))

            # Introduce a delay between each batch of link crawls
            await asyncio.gather(*tasks)  # Execute all crawls in parallel

    await crawl(params.base_url, 0)
    return all_pages


async def save_pages_to_mongo(all_pages: list[WebPage]):
    unique_links = set()
    for page in all_pages:
        if page.url not in unique_links:
            await WebPage.insert(page)
            unique_links.add(page.url)

    return unique_links


def process_documents(documents):
    processed_docs = []
    processed_ids = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)

    for doc in documents:
        content = doc.content
        url = doc.url
        title = doc.title
        keywords = doc.keywords

        # Create a single text block from the content
        text = f"Title: {title}\nKeywords: {keywords}\nContent: {content}"

        # Chunk the content
        chunks = text_splitter.split_text(text)

        for chunk in chunks:
            processed_docs.append(Document(
                page_content=chunk, metadata={
                    'title': title, "keywords": keywords, "url": url}
            ))
            processed_ids.append(str(uuid.uuid4()))

    return processed_docs, processed_ids


async def store_in_vector_db():
    # Fetch documents from MongoDB
    documents = await WebPage.fetch_documents()
    # Process the documents (clean and chunk)
    processed_docs, processed_ids = process_documents(documents)
    index = pc.Index(settings.VECTOR_INDEX_NAME)
    vector_store = PineconeVectorStore(index=index, embedding=ai_embedding)
    vector_store.add_documents(documents=processed_docs, ids=processed_ids)
