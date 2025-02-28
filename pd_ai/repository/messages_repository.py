import datetime
from psycopg.types.json import Json
from pd_ai import models
from .db import get_db_connection


def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


async def create(message: models.MessageBase) -> models.Message:
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO messages (content) VALUES (%s) RETURNING id, content",
                (Json(message.content),),
            )
            row = await cursor.fetchone()
            if row is None:
                raise Exception("Failed to insert message")
            return models.Message(id=row[0], content=row[1])


async def get_all() -> list[models.Message]:
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id, content FROM messages")
            rows = await cursor.fetchall()
            return [models.Message(id=row[0], content=row[1]) for row in rows]
