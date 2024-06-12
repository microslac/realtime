from typing import Annotated

from fastapi import Body, Depends
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter

from app.websocket.constants import SocketType
from app.websocket.contexts.queue import QueueContext
from app.websocket.services import websocket
from app.websocket.socket.stores import keys

router = RabbitRouter()
exchange = RabbitExchange("communication", type=ExchangeType.TOPIC)

message_queue = RabbitQueue("realtime.message", routing_key="message", durable=True)
user_profile_queue = RabbitQueue("realtime.user.profile.event", routing_key="user.profile.{event}", durable=True)
channel_member_queue = RabbitQueue("realtime.channel.member.event", routing_key="channel.member.{event}", durable=True)


@router.subscriber(message_queue, exchange)
async def message_handler(payload: Annotated[dict, Body()], ctx: Annotated[QueueContext, Depends()]):
    await websocket.consume(SocketType.MESSAGE, payload=payload, ctx=ctx)


@router.subscriber(user_profile_queue, exchange)
async def user_profile_handler(payload: Annotated[dict, Body()], ctx: Annotated[QueueContext, Depends()]):
    await websocket.consume(SocketType.USER_PROFILE_CHANGED, payload=payload, ctx=ctx)


@router.subscriber(channel_member_queue, exchange)
async def channel_member_handler(payload: Annotated[dict, Body()], ctx: Annotated[QueueContext, Depends()]):
    await websocket.store.delete(keys.channel_members.format(payload.get("channel")))
    await websocket.consume(SocketType.CHANNEL_MEMBER_JOINED, payload=payload, ctx=ctx)
