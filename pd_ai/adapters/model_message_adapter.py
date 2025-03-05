from pydantic_ai.messages import ModelMessage
from pd_ai.repository import messages_repository
from pd_ai.helpers import ModelMessageTypeAdapter
from pd_ai import models
import dataclasses


async def get_messages() -> list[ModelMessage]:
    db_messages = await messages_repository.get_all()
    return [ModelMessageTypeAdapter.validate_python(m.content) for m in db_messages]


async def save_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
    new_messages = [
        await messages_repository.create(
            models.MessageBase(content=dataclasses.asdict(m))
        )
        for m in messages
    ]
    return [ModelMessageTypeAdapter.validate_python(m.content) for m in new_messages]
