from pinecone import Pinecone, ServerlessSpec
from config import settings


def init_pinecone() -> None:
    pc = Pinecone(api_key=settings.PINECONE_API_KEY,)
    indexes = [item.name for item in pc.list_indexes()]
    if settings.VECTOR_INDEX_NAME not in indexes:
        pc.create_index(
            name=settings.VECTOR_INDEX_NAME,
            dimension=3072,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    return pc


pc = init_pinecone()
