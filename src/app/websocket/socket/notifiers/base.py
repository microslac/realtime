from __future__ import annotations

from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    async def notify(self, connection_id: str, payload: dict, **kwargs) -> str | None:
        pass

    @abstractmethod
    async def notify_many(self, connection_ids: list[str], payload: dict, **kwargs) -> list | None:
        pass

    async def is_enabled(self) -> bool:
        return True

    @staticmethod
    def factory(notifier_type: str = "") -> Notifier:
        from .noop import NoopNotifier
        from .socket import SocketNotifier

        if notifier_type == "socket":
            return SocketNotifier()
        return NoopNotifier()


class NotifyError(Exception):
    def __init__(self, connection_id: str):
        self.connection_id = connection_id

    def __str__(self):
        return str(self.connection_id)
