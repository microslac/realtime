from app.websocket.constants import PresenceStatus, SocketType
from app.websocket.services import presence
from app.websocket.socket import Handler, keys


class PresenceSubHandler(Handler):
    async def handle(self) -> None:
        user_ids = self.ctx.data.get("users", [])
        if user_ids:
            await self.echo_presences(user_ids)
            keys_ = [keys.user_subs.format(uid) for uid in user_ids]  # subscribe
            await self.store.add_many(keys=keys_, value=self.ctx.connection_id)

    async def echo_presences(self, user_ids: list[str]) -> None:
        payload = dict(type=SocketType.PRESENCE_CHANGED)
        active_ids, away_ids = await presence.partition_presence(user_ids)
        if active_ids:
            payload.update(users=active_ids, presence=PresenceStatus.ACTIVE)
            await self.notifier.notify(self.ctx.connection_id, payload=payload)
        if away_ids:
            payload.update(users=away_ids, presence=PresenceStatus.AWAY)
            await self.notifier.notify(self.ctx.connection_id, payload=payload)
