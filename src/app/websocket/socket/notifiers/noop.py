from .base import Notifier


class NoopNotifier(Notifier):
    def is_enabled(self) -> bool:
        return True

    async def notify(self, connection_id: str, payload: dict, **kwargs) -> str | None:
        return None

    async def notify_many(self, connection_ids: list[str], payload: dict, **kwargs) -> list | None:
        return None
