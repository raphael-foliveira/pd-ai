from pydantic_ai.messages import ModelMessage
import pydantic

ModelMessageTypeAdapter = pydantic.TypeAdapter(ModelMessage)
