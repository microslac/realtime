from __future__ import annotations

from .base import Store

from app.redis import Redis, get_connection_pool, redis_pipeline


class ClientDescriptor:
    def __get__(self, instance: RedisStore, cls: type[RedisStore]):
        if instance is None:
            return self

        connection_pool = get_connection_pool(instance.database)
        client = instance.client = Redis(connection_pool=connection_pool)
        return client


class RedisStore(Store):
    client: Redis = ClientDescriptor()
    ttl = 3600 * 6  # unit: seconds
    database: int = 1
    namespace: str = ""

    def __init__(self, namespace: str = "", database: int = 1):
        self.namespace = namespace
        self.database = database

    def gen_key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    async def set(self, key: str, value: str, ttl: int = 0) -> None:
        key = self.gen_key(key)
        ttl = ttl or self.ttl
        async with redis_pipeline(self.client) as pipe:
            await pipe.set(key, value=value).expire(key, ttl)

    async def get(self, key: str) -> str:
        key = self.gen_key(key)
        value = await self.client.get(key)
        return value and value.decode("utf-8")

    async def mget(self, key: str, fields: list[str] = None) -> dict:
        key = self.gen_key(key)
        if fields:
            values = await self.client.hmget(key, fields)
            return dict(zip(fields, [v.decode("utf-8") for v in values]))
        else:
            entries = await self.client.hgetall(key)
            return {k.decode("utf-8"): v.decode("utf-8") for k, v in entries.items()}

    async def delete(self, key: str) -> None:
        key = self.gen_key(key)
        await self.client.unlink(key)

    async def add(self, key: str, value: str) -> None:
        key = self.gen_key(key)
        async with redis_pipeline(self.client) as pipe:
            await pipe.sadd(key, value).expire(key, self.ttl)

    async def add_all(self, key: str, values: list[str]) -> None:
        key = self.gen_key(key)
        async with redis_pipeline(self.client) as pipe:
            await pipe.sadd(key, *values).expire(key, self.ttl)

    async def add_many(self, keys: list[str], value: str) -> None:
        keys = [self.gen_key(k) for k in keys]
        async with redis_pipeline(self.client) as pipe:
            for key in keys:
                await pipe.sadd(key, value).expire(key, self.ttl)

    async def remove(self, key: str, values: list[str]) -> None:
        if key and values:
            key = self.gen_key(key)
            async with redis_pipeline(self.client) as pipe:
                await pipe.srem(key, *values)

    async def remove_many(self, keys: list[str], values: list[str]) -> None:
        if keys and values:
            keys = [self.gen_key(k) for k in keys]
            async with redis_pipeline(self.client) as pipe:
                for key in keys:
                    await pipe.srem(key, *values)

    async def exists(self, key: str) -> bool:
        value = await self.client.exists(self.gen_key(key))
        return bool(value)

    async def all(self, key: str) -> list[str]:
        if await self.exists(key):
            key = self.gen_key(key)
            return [str(v.decode("utf-8")) for v in await self.client.smembers(key)]
        return []

    async def clear(self, key: str) -> None:
        key = self.gen_key(key)
        await self.client.unlink(key)
