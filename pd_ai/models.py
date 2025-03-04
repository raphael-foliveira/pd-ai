from pydantic import BaseModel
from typing_extensions import TypedDict


class LLMMessage(TypedDict):
    kind: str
    parts: list[dict]


class MessageBase(BaseModel):
    content: dict


class Message(MessageBase):
    id: int


class EmbeddingBase(BaseModel):
    embedding: list[float]
    text: str


class Embedding(EmbeddingBase):
    id: int
