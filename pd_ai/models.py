from pydantic import BaseModel


class MessageBase(BaseModel):
    content: list[dict] | dict


class Message(MessageBase):
    id: int


class EmbeddingBase(BaseModel):
    embedding: list[float]
    text: str


class Embedding(EmbeddingBase):
    id: int
