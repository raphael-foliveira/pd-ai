from pd_ai import models
from .db import execute_and_fetchall, execute_and_fetchone
import json


async def create(embedding: models.EmbeddingBase) -> models.Embedding:
    row = await execute_and_fetchone(
        """
        INSERT INTO embeddings (embedding, text) VALUES ($1, $2) RETURNING id, embedding, text;
        """,
        (json.dumps(embedding.embedding), embedding.text),
    )
    if row is None:
        raise Exception("Failed to insert embedding")
    return models.Embedding(
        id=row[0],
        embedding=row[1],
        text=row[2],
    )


async def similarity_search(
    search_query: str, limit: int = 5
) -> list[models.Embedding]:
    rows = await execute_and_fetchall(
        """
            SELECT id, embedding, text FROM embeddings ORDER BY embedding <-> $1 limit $2;
        """,
        (search_query, limit),
    )
    return [models.Embedding(id=row[0], embedding=row[1], text=row[2]) for row in rows]
