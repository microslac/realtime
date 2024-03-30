from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.websocket.contexts.api import ApiContext
from app.websocket.services import websocket

router = APIRouter(prefix="/ws")


@router.post("/connect", status_code=status.HTTP_200_OK)
async def connect(ctx: Annotated[ApiContext, Depends()]):
    response = await websocket.connect(ctx)
    return response


@router.post("/callback", status_code=status.HTTP_200_OK)
async def callback(ctx: Annotated[ApiContext, Depends()]):
    response = await websocket.callback(ctx)
    return response


@router.post("/disconnect", status_code=status.HTTP_200_OK)
async def disconnect(ctx: Annotated[ApiContext, Depends()]):
    response = await websocket.disconnect(ctx)
    return response
