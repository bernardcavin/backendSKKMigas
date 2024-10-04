from app.api.auth import routes as auth_routes
from app.api.job import routes as job_routes
from app.api.spatial import routes as spatial_routes
from app.api.well import routes as well_routes
from app.api.utils import routes as utils_routes
from app.api.dashboard import routes as dashboard_routes
from app.api.visualize import routes as visualization_routes
from fastapi.middleware.cors import CORSMiddleware
from app.core.database_functions import init_db
from app.core.error_handlers import (
    custom_http_exception_handler, 
    custom_exception_handler, 
    sqlalchemy_exception_handler,
    custom_request_validation_exception_handler,
    custom_starlette_http_exception_handler,
    validation_exception_handler
)
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError
from fastapi.routing import APIRoute
from app.core.config import settings
import os

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

if settings.app_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.app_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
init_db()
os.makedirs(settings.upload_dir, exist_ok=True)


app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(Exception, custom_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(RequestValidationError, custom_request_validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_starlette_http_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)

app.include_router(auth_routes.router, prefix=settings.API_V1_STR)
app.include_router(job_routes.router, prefix=settings.API_V1_STR)
app.include_router(spatial_routes.router, prefix=settings.API_V1_STR)
app.include_router(well_routes.router, prefix=settings.API_V1_STR)
app.include_router(utils_routes.router, prefix=settings.API_V1_STR)
app.include_router(dashboard_routes.router, prefix=settings.API_V1_STR)
app.include_router(visualization_routes.router, prefix=settings.API_V1_STR)
