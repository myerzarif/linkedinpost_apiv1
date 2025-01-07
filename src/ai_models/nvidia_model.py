from .base import BaseModel
from config import settings
from langchain_nvidia_ai_endpoints import ChatNVIDIA


class NvidiaModel(BaseModel):
    def __init__(self):
        self.model = "meta/llama3-70b-instruct"

    def get_model(self):
        return ChatNVIDIA(model=self.model)

    def get_embedding(self):
        return None