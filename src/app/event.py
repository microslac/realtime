import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter

from app.settings import settings
from app.websocket.events.communication import router as communication_router
from app.websocket.services import presence


@asynccontextmanager
async def lifespan(app: FastAPI):
    pubsub = await presence.subscribe()
    task = asyncio.create_task(pubsub.run())
    yield
    task.cancel()
    await task


event_router = RabbitRouter(settings.rabbit.url, lifespan=lifespan)

event_router.include_router(communication_router)
