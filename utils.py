from fastapi import Request

from typing import Optional, Any

from pydantic import BaseModel
from starlette.responses import JSONResponse


class Response(BaseModel):
    success: bool
    data: Optional[Any]
    error: Optional[str]


class UvicornException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


async def http_exception_handler(request: Request, exception: UvicornException):
    return JSONResponse(status_code=exception.status_code,
                        content=Response(success=False, data=None, error=exception.message).model_dump())
