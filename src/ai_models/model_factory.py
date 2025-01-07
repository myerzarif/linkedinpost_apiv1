from .openai_model import OpenAIModel
from .cohere_model import CohereModel
from .anthropic_model import AnthropicModel
from .nvidia_model import NvidiaModel
from models.enums import AIModelEnum


class ModelFactory:
    @staticmethod
    def get_aimodel(model_name: str):
        if model_name == AIModelEnum.OPENAI.value:
            return OpenAIModel()
        elif model_name == AIModelEnum.COHERE.value:
            return CohereModel()
        elif model_name == AIModelEnum.ANTHROPIC.value:
            return AnthropicModel()
        elif model_name == AIModelEnum.NVIDIA.value:
            return NvidiaModel()
        else:
            raise ValueError(f"Model {model_name} is not supported")


# aimodel = ModelFactory.get_aimodel(AIModelEnum.COHERE.value)
aimodel = ModelFactory.get_aimodel(AIModelEnum.OPENAI.value)
model = aimodel.get_model()
embedding =  aimodel.get_embedding()