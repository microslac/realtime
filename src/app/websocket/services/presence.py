from datetime import datetime

from app.websocket.constants import SocketType
from app.websocket.socket import Publisher
from app.websocket.socket.notifiers.socket import SocketNotifier
from app.websocket.socket.stores.redis import RedisStore

store = RedisStore(database=0, namespace="presence")
notifier = SocketNotifier()


def exception_handler(*args, **kwargs):
    pass  # TODO: log


async def partition_presence(user_ids: list[str]) -> tuple[list, list]:
    active_ids = {uid for uid in user_ids if await store.exists(uid)}
    away_ids = set(user_ids) - active_ids
    return list(active_ids), list(away_ids)


async def publish_presence(user_id: str, active: bool = False):
    from app.websocket.services import websocket

    # Only store "presence:{}" keys in redis database 0.
    # Other data related keys are store in database 1.
    publisher = Publisher.factory(
        SocketType.PRESENCE_CHANGED,
        payload=dict(users=[user_id], active=active),
        notifier=websocket.notifier,
        store=websocket.store,
        ctx=None,
    )
    await publisher.publish()


async def key_expired_handler(message):
    key = message.get("data", b"").decode("utf-8")
    if key.startswith("presence:"):
        if user_id := key.split(":").pop():
            await publish_presence(user_id, False)


async def subscribe():
    pubsub = store.client.pubsub()
    await pubsub.psubscribe(**{"__keyevent@0__:expired": key_expired_handler})
    return pubsub


async def heartbeat(user_id: str, active: bool = False, publish: bool = True) -> None:
    ts = await store.get(key=user_id)

    if active:
        # Expand ttl to avoid key expiration
        base = 10
        leeway = 2
        interval = 2
        value = str(datetime.utcnow().timestamp())
        await store.set(key=user_id, value=value, ttl=base * interval + leeway)
        if not ts:
            # User just login, publish event
            await publish_presence(user_id, True)
    else:
        if ts:
            # User just logoff as intended
            await store.delete(key=user_id)
            await publish_presence(user_id, False)
