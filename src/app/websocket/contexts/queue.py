from typing import Annotated, Optional

from fastapi import BackgroundTasks, Body, Depends
from faststream import Path

from app.database import Session, db_session


class QueueContext:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        payload: Annotated[dict, Body()],
        db: Annotated[Session, Depends(db_session)],
        event: Annotated[Optional[str], Path()] = None,
    ):
        self.db = db
        self.event = event
        self.payload = payload
        self.background_tasks = background_tasks
