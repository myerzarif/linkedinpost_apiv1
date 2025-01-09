from .base import BaseModel
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings


class OpenAIModel(BaseModel):
    def __init__(self):
        self.model = "gpt-4o-mini"

    def get_model(self):
        return ChatOpenAI(model=self.model)

    def get_embedding(self):
        # text-embedding-ada-002
        return OpenAIEmbeddings(model="text-embedding-3-large")