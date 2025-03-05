import json
from psycopg.types.json import Json
from pd_ai import models
from .db import execute_and_fetchall, execute_and_fetchone


async def create(message: models.MessageBase) -> models.Message:
    row = await execute_and_fetchone(
        "INSERT INTO messages (content) VALUES (%s) RETURNING id, content",
        (Json(message.content, dumps=_dumps),),
    )
    if row is None:
        raise Exception("Failed to insert message")
    return models.Message(id=row[0], content=row[1])


async def get_all() -> list[models.Message]:
    rows = await execute_and_fetchall("SELECT id, content FROM messages ORDER BY id")
    return [models.Message(id=row[0], content=row[1]) for row in rows]


def _dumps(obj):
    return json.dumps(obj, default=str)
