from .base import BaseModel
from config import settings
from langchain_cohere import ChatCohere
from langchain_cohere.embeddings import CohereEmbeddings


class CohereModel(BaseModel):
    def __init__(self):
        self.model = "command-r-plus"

    def get_model(self):
        return ChatCohere(model=self.model)

    def get_embedding(self):
        return CohereEmbeddings(model="embed-english-light-v3.0")
