from pydantic_ai.messages import ModelMessage, ModelMessagesTypeAdapter
from pd_ai.repository import messages_repository
from pd_ai import models


async def get_messages() -> list[ModelMessage]:
    output: list[ModelMessage] = []
    db_messages = await messages_repository.get_all()
    for message in db_messages:
        output.extend(ModelMessagesTypeAdapter.validate_python(message.content))
    return output


async def save_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
    new_message_entry = await messages_repository.create(
        models.MessageBase(content=ModelMessagesTypeAdapter.dump_python(messages))
    )
    return ModelMessagesTypeAdapter.validate_python(new_message_entry.content)
