from .base import Store


class NoopStore(Store):
    async def set(self, key: str, value: dict) -> None:
        return None

    async def get(self, key: str) -> None:
        return None

    async def delete(self, key: str) -> None:
        return None

    async def add(self, key: str, value: str) -> None:
        return None

    async def add_all(self, key, values: list[str]) -> None:
        pass

    async def add_many(self, keys: list[str], value: str) -> None:
        return None

    async def remove(self, key: str, values: list[str]) -> None:
        return None

    async def remove_many(self, keys: list[str], values: list[str]) -> None:
        return None

    async def all(self, key: str) -> list[str]:
        return []

    async def exists(self, key: str) -> bool:
        return False

    async def clear(self, key: str) -> None:
        return None
