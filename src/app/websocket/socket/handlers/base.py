from __future__ import annotations

from abc import ABC, abstractmethod

from app.patterns.null import Null
from app.websocket.constants import SocketType
from app.websocket.contexts import ApiContext
from app.websocket.socket.notifiers import Notifier
from app.websocket.socket.stores import Store


class Handler(ABC):
    def __init__(self, ctx: ApiContext, store: Store, notifier: Notifier, **kwargs):
        self.ctx = ctx
        self.store = store
        self.notifier = notifier

    @abstractmethod
    async def handle(self, **kwargs) -> dict:
        pass

    @staticmethod
    def factory(socket_type: SocketType, ctx: ApiContext, store: Store, notifier: Notifier, **kwargs) -> Handler:
        from .connect import ConnectHandler
        from .disconnect import DisconnectHandler
        from .ping import PingHandler
        from .presence_sub import PresenceSubHandler
        from .user_typing import UserTypingHandler

        handler_mapping = {
            SocketType.PING: PingHandler,
            SocketType.CONNECT: ConnectHandler,
            SocketType.DISCONNECT: DisconnectHandler,
            SocketType.PRESENCE_SUB: PresenceSubHandler,
            SocketType.USER_TYPING: UserTypingHandler,
        }

        handler_cls = handler_mapping.get(socket_type, Null)
        return handler_cls(ctx, store, notifier, **kwargs)
