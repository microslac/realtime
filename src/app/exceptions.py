from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


class NotAuthenticated(HTTPException):
    def __init__(self, headers=None):
        detail = dict(ok=False, error="unauthenticated")
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail, headers=headers)


async def not_found(request, exc):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]})


exception_handlers = {404: not_found, RateLimitExceeded: _rate_limit_exceeded_handler}

limiter = Limiter(key_func=get_remote_address)
