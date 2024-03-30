from app.websocket.constants import SocketType
from app.websocket.services import presence
from app.websocket.socket import Handler, keys


class PingHandler(Handler):
    async def handle(self, **kwargs) -> dict:
        connection_id = self.ctx.connection_id
        user_id = await self.store.get(key=keys.conns.format(connection_id))
        if user_id:
            payload = dict(type=SocketType.PONG)
            await presence.heartbeat(user_id=user_id, active=True)
            await self.notifier.notify(connection_id, payload=payload)
        return {}
