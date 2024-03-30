import requests
from jwt import decode

from .base import Handler

from app.exceptions import NotAuthenticated
from app.schemas.token import Token
from app.settings import settings
from app.websocket.constants import SocketType
from app.websocket.services import presence
from app.websocket.socket.stores import keys


class ConnectHandler(Handler):
    type = SocketType.CONNECT

    async def handle(self, **kwargs) -> dict:
        token = await self.authenticate()
        connection_id = self.ctx.connection_id
        await presence.heartbeat(user_id=token.user, active=True)
        await self.store.set(key=keys.conns.format(connection_id), value=token.user)
        await self.store.add(key=keys.user_conns.format(token.user), value=connection_id)
        self.ctx.background_tasks.add_task(self.handshake, connection_id)
        return {}

    async def authenticate(self) -> Token:
        jwt = self.ctx.data.get("token")
        headers = {"Authorization": f"Token {jwt}"}
        auth_verify_url = "http://auth:8011/auth/verify"
        response = requests.post(auth_verify_url, headers=headers)
        data = response.json()
        if data.get("ok"):
            decoded = decode(jwt, options={"verify_signature": False})
            token = Token(**decoded)
            return token
        raise NotAuthenticated()

    async def handshake(self, connection_id: str):
        payload = dict(type=SocketType.HELLO, region=settings.websocket.region, start=True)
        await self.notifier.notify(connection_id=connection_id, payload=payload)
