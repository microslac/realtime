from contextlib import asynccontextmanager
from string import digits

from redis.asyncio import ConnectionPool, Redis

from app.settings import settings

connection_pool = ConnectionPool.from_url(settings.redis.url)


def get_connection_pool(database=settings.redis.database) -> ConnectionPool:
    assert database in list(range(0, 16))
    url_at_database = settings.redis.url.rstrip(digits) + str(database)
    return ConnectionPool.from_url(url_at_database)


def redis_client():
    client: Redis = Redis(connection_pool=connection_pool)
    try:
        yield client
    finally:
        client.close()


@asynccontextmanager
async def redis_pipeline(redis: Redis):
    pipeline = await redis.pipeline()

    try:
        yield pipeline
    finally:
        await pipeline.execute()
