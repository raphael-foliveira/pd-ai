import logging
from dotenv import load_dotenv

load_dotenv()

import asyncio
from pd_ai.agent import agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.messages import (
    ModelMessage,
    ToolCallPart,
)
from pd_ai.repository import db
from pd_ai.adapters import model_message_adapter


def print_all_messages(response: AgentRunResult[str]):
    for m in response.all_messages():
        for p in m.parts:
            if isinstance(p, ToolCallPart):
                print(f"Tool: {p.tool_name}")
                print(f"Args: {p.args}")
            else:
                print(f"System: {p.content}")


async def chat_loop():
    while True:
        user_prompt = input("User: ")
        if user_prompt in ["exit", "quit"]:
            print("bye!")
            break

        messages: list[ModelMessage] = await model_message_adapter.get_messages()
        response = await agent.run(
            user_prompt=user_prompt,
            message_history=messages,
            deps={},
        )
        new_messages: list[ModelMessage] = response.new_messages()
        await model_message_adapter.save_messages(new_messages)
        print(f"Bot: {response.data}")


async def main():
    await db.pool.open()
    await db.create_tables()
    try:
        await chat_loop()
    except Exception:
        logging.exception("An error occurred in the chat loop")
    finally:
        await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())
