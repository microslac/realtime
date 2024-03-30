import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.event import event_router
from app.exceptions import exception_handlers, limiter
from app.settings import settings

app = FastAPI(
    title="realtime",
    description="realtime",
    exception_handlers=exception_handlers,
    lifespan=event_router.lifespan_context,
    limiter=limiter,
)

app.include_router(api_router)

app.include_router(event_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.api.host, port=settings.api.port, reload=True)
