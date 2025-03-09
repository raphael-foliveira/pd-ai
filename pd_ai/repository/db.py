from contextlib import asynccontextmanager
from psycopg.abc import Params, Query
from psycopg_pool import AsyncConnectionPool
from typing_extensions import LiteralString

import config

pool = AsyncConnectionPool(
    conninfo=config.DATABASE_URL,
    open=False,
    min_size=1,
    max_size=10,
)


@asynccontextmanager
async def get_db_connection():
    async with pool.connection() as connection:
        yield connection


@asynccontextmanager
async def get_db_cursor():
    async with get_db_connection() as connection:
        async with connection.cursor() as cursor:
            yield cursor


async def execute_query(query: LiteralString, params: Params | None = None):
    async with get_db_cursor() as cursor:
        await cursor.execute(query=query, params=params)


async def execute_and_fetchall(query: Query, params: Params | None = None):
    async with get_db_cursor() as cursor:
        await cursor.execute(query=query, params=params)
        return await cursor.fetchall()


async def execute_and_fetchone(query: LiteralString, params: Params | None = None):
    async with get_db_cursor() as cursor:
        await cursor.execute(query=query, params=params)
        return await cursor.fetchone()


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
