from pd_ai import models
from .db import get_db_connection
import json


async def create(embedding: models.EmbeddingBase) -> models.Embedding:
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO embeddings (embedding, text) VALUES ($1, $2) RETURNING id, embedding, text;
                """,
                (json.dumps(embedding.embedding), embedding.text),
            )
            row = await cursor.fetchone()
            if row is None:
                raise Exception("Failed to inser embedding")
            return models.Embedding(
                id=row[0],
                embedding=row[1],
                text=row[2],
            )


async def similarity_search(
    search_query: str, limit: int = 5
) -> list[models.Embedding]:
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                SELECT id, embedding, text FROM embeddings ORDER BY embedding <-> $1 limit $2;
            """,
                (search_query, limit),
            )
            rows = await cursor.fetchall()
            return [
                models.Embedding(id=row[0], embedding=row[1], text=row[2])
                for row in rows
            ]
