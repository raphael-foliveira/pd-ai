import asyncio
import json
from pd_ai import models
from pd_ai.repository import messages_repository
from pd_ai.agent import agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter,
    ToolCallPart,
)
from dotenv import load_dotenv
from pd_ai.repository import db

load_dotenv()


def print_all_messages(response: AgentRunResult[str]):
    for m in response.all_messages():
        for p in m.parts:
            if isinstance(p, ToolCallPart):
                print(f"Tool: {p.tool_name}")
                print(f"Args: {p.args}")
            else:
                print(f"System: {p.content}")


async def get_messages() -> list[ModelMessage]:
    db_messages = await messages_repository.get_all()
    messages: list[ModelMessage] = []
    for db_message in db_messages:
        json_message = json.dumps(db_message.content, default=str).encode()
        messages.extend(ModelMessagesTypeAdapter.validate_json(json_message))
    return messages


async def save_messages(messages: list[ModelMessage]):
    messages_json = ModelMessagesTypeAdapter.dump_json(messages)
    await messages_repository.create(
        models.MessageBase(content=json.loads(messages_json.decode()))
    )


async def chat_loop():
    while True:
        user_prompt = input("User: ")
        if user_prompt in ["exit", "quit"]:
            print("bye!")
            break

        messages: list[ModelMessage] = await get_messages()
        response = await agent.run(
            user_prompt=user_prompt,
            message_history=messages,
            deps={},
        )
        new_messages: list[ModelMessage] = response.new_messages()
        await save_messages(new_messages)
        print(f"Bot: {response.data}")


async def main():
    await db.pool.open()
    await db.create_tables()
    try:
        await chat_loop()
    finally:
        await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())
