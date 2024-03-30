from typing import Annotated, Optional

from fastapi import BackgroundTasks, Body, Depends

from app.database import Session, db_session
from app.websocket.deps import get_connection_id


class ApiContext:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        db: Annotated[Session, Depends(db_session)],
        connection_id: Annotated[str, Depends(get_connection_id)],
        data: Annotated[Optional[dict], Body()] = None,
    ):
        self.db = db
        self.data = data
        self.connection_id = connection_id
        self.background_tasks = background_tasks
