from __future__ import annotations

from abc import ABC, abstractmethod

from app.patterns.null import Null
from app.websocket.constants import SocketType
from app.websocket.contexts import QueueContext
from app.websocket.socket import Notifier, Store


class Publisher(ABC):
    def __init__(self, payload: dict, store: Store, notifier: Notifier, ctx: QueueContext = None, **kwargs):
        self.payload = payload
        self.ctx = ctx
        self.store = store
        self.notifier = notifier

    @abstractmethod
    async def publish(self) -> dict:
        pass

    @staticmethod
    def factory(
        socket_type: SocketType, payload: dict, store: Store, notifier: Notifier, ctx: QueueContext = None, **kwargs
    ) -> Publisher:
        from .channel_member_joined import ChannelMemberJoinedPublisher
        from .message import MessagePublisher
        from .presence_changed import PresenceChangedPublisher
        from .user_profile_changed import UserProfileChangedPublisher

        publisher_mapping = {
            SocketType.MESSAGE: MessagePublisher,
            SocketType.PRESENCE_CHANGED: PresenceChangedPublisher,
            SocketType.CHANNEL_MEMBER_JOINED: ChannelMemberJoinedPublisher,
            SocketType.USER_PROFILE_CHANGED: UserProfileChangedPublisher,
        }

        publisher_cls = publisher_mapping.get(socket_type, Null)
        return publisher_cls(payload, store, notifier, ctx, **kwargs)
