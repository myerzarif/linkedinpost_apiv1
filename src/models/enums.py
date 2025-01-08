
from enum import Enum


class EnvEnum(Enum):
    DEV = "DEV"
    STAGE = "STAGE"
    PRODUCTION = "PRODUCTION"


class HttpMethod(Enum):
    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"
    PUT = "PUT"


class HttpContentType(Enum):
    FORM = "FORM"
    JSON = "JSON"


class AIModelEnum(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    ANTHROPIC = "ANTHROPIC"
    NVIDIA = "NVIDIA"
