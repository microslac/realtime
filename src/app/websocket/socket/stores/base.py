from __future__ import annotations

from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    async def get(self, key: str) -> str:
        pass

    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def add(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    async def add_all(self, key, values: list[str]) -> None:
        pass

    @abstractmethod
    async def add_many(self, keys: list[str], value: str) -> None:
        pass

    @abstractmethod
    async def remove(self, key: str, values: list[str]) -> None:
        pass

    @abstractmethod
    async def remove_many(self, keys: list[str], values: list[str]) -> None:
        pass

    @abstractmethod
    async def all(self, key: str) -> list[str]:
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def clear(self, key: str) -> None:
        pass

    @staticmethod
    def factory(store_type: str = "", **kwargs) -> Store:
        from .noop import NoopStore
        from .redis import RedisStore

        if store_type == "redis":
            return RedisStore(**kwargs)
        return NoopStore()
