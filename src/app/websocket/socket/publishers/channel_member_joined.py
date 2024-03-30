from .base import Publisher

from app.websocket.constants import SocketType
from app.websocket.socket.stores import keys


class ChannelMemberJoinedPublisher(Publisher):
    def clean(self):
        user = self.ctx.payload.get("user")
        channel = self.ctx.payload.get("channel")
        members = self.ctx.payload.pop("members", [])  # consume
        is_valid = all([channel, user, members])
        return is_valid, channel, user, members

    async def publish(self) -> dict:
        is_valid, channel, user, members = self.clean()
        if is_valid:
            payload = dict(type=SocketType.CHANNEL_MEMBER_JOINED, **self.payload)
            for member in members:
                connection_ids = await self.store.all(keys.user_conns.format(member))
                invalid_connection_ids = await self.notifier.notify_many(list(connection_ids), payload=payload)
                await self.store.remove(key=keys.user_conns.format(user), values=invalid_connection_ids)
        return {}
