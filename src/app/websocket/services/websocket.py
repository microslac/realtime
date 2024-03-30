from app.websocket.constants import SocketType
from app.websocket.contexts import ApiContext, QueueContext
from app.websocket.socket import Handler, Notifier, Publisher, Store

store = Store.factory("redis", namespace="ws")
notifier = Notifier.factory("socket")


async def connect(ctx: ApiContext) -> dict:
    socket_type = SocketType.CONNECT
    handler = Handler.factory(socket_type, ctx=ctx, store=store, notifier=notifier)
    return await handler.handle()


async def callback(ctx: ApiContext) -> dict:
    socket_type = ctx.data.get("type")
    handler = Handler.factory(socket_type, ctx=ctx, store=store, notifier=notifier)
    return await handler.handle()


async def disconnect(ctx: ApiContext) -> dict:
    socket_type = SocketType.DISCONNECT
    handler = Handler.factory(socket_type, ctx=ctx, store=store, notifier=notifier)
    return await handler.handle()


async def consume(socket_type: SocketType, payload: dict, ctx: QueueContext = None) -> dict:
    publisher = Publisher.factory(socket_type, payload=payload, ctx=ctx, store=store, notifier=notifier)
    return await publisher.publish()
