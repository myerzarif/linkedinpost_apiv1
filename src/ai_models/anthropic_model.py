from .base import BaseModel
from config import settings
from langchain_anthropic import ChatAnthropic


class AnthropicModel(BaseModel):
    def __init__(self):
        self.model = "claude-3-5-sonnet-20240620"

    def get_model(self):
        return ChatAnthropic(model=self.model)

    def get_embedding(self):
        return None