import datetime
import json
from psycopg.types.json import Json
from pd_ai import models
from .db import execute_and_fetchall, execute_and_fetchone


def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


async def create(message: models.MessageBase) -> models.Message:
    row = await execute_and_fetchone(
        "INSERT INTO messages (content) VALUES (%s) RETURNING id, content",
        (Json(message.content, dumps=lambda c: json.dumps(c, default=str)),),
    )
    if row is None:
        raise Exception("Failed to insert message")
    return models.Message(id=row[0], content=row[1])


async def get_all() -> list[models.Message]:
    rows = await execute_and_fetchall("SELECT id, content FROM messages")
    return [models.Message(id=row[0], content=row[1]) for row in rows]
