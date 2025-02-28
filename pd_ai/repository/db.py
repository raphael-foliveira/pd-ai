from contextlib import asynccontextmanager
import os
from typing_extensions import LiteralString
from psycopg_pool import AsyncConnectionPool

pool = AsyncConnectionPool(
    conninfo=os.getenv("DATABASE_URL") or "",
    open=False,
    min_size=1,
    max_size=10,
)


@asynccontextmanager
async def get_db_connection():
    async with pool.connection() as connection:
        yield connection


async def execute_query(query: LiteralString, *args):
    async with get_db_connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(query=query, params=args)


async def create_tables():
    await execute_query(
        """
            CREATE EXTENSION IF NOT EXISTS vector;

            CREATE TABLE IF NOT EXISTS embeddings (
                id SERIAL PRIMARY KEY,
                embedding VECTOR(1536) NOT NULL,
                text VARCHAR NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                content JSONB NOT NULL
            )
        """
    )
