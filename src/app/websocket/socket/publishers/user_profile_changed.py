from app.websocket.constants import SocketType
from app.websocket.socket import Publisher, keys


class UserProfileChangedPublisher(Publisher):
    async def publish(self) -> dict:
        user_id = self.payload.get("id")
        payload = dict(type=SocketType.USER_PROFILE_CHANGED, user=self.payload)
        subscriber_connection_ids = await self.store.all(keys.user_subs.format(user_id))
        invalid_connection_ids = await self.notifier.notify_many(subscriber_connection_ids, payload=payload)
        if invalid_connection_ids:
            await self.store.remove(key=keys.user_subs.format(user_id), values=invalid_connection_ids)
        return {}
