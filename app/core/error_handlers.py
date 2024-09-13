from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import logging
from starlette.exceptions import HTTPException as StarletteHTTPException

async def custom_starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

async def custom_http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

async def custom_request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": exc.errors()},
    )

async def custom_exception_handler(request: Request, exc: Exception):
    # Log unexpected errors
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "An unexpected error occurred. Please try again later."}
    )

# SQLAlchemy Error Handler if you want to handle database errors specifically
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "A database error occurred. Please contact support."}
    )