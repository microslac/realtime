from app.websocket.constants import PresenceStatus, SocketType
from app.websocket.socket import Publisher, keys


class PresenceChangedPublisher(Publisher):
    async def publish(self) -> dict:
        active = self.payload.get("active", False)
        user_ids = self.payload.get("users") or []
        presence = PresenceStatus.ACTIVE if active else PresenceStatus.AWAY
        payload = dict(type=SocketType.PRESENCE_CHANGED, users=user_ids, presence=presence)

        for user_id in user_ids:
            subscriber_cids = await self.store.all(key=keys.user_subs.format(user_id))
            invalid_connection_ids = await self.notifier.notify_many(subscriber_cids, payload=payload)
            if invalid_connection_ids:
                await self.store.remove(key=keys.user_subs.format(user_id), values=invalid_connection_ids)
        return {}
