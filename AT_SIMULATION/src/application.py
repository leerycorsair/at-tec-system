import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.exceptions import RequestValidationError

from src.client.auth_client import AuthClientSingleton
from src.delivery.core.middleware.cors import cors_middleware
from src.delivery.core.middleware.fastapi_exception_handler import (
    validation_exception_handler,
)
from src.delivery.core.middleware.request_dump import request_dump
from .delivery.router import setup_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_routes(app)
    # Initialize resources like database connections
    # setup_storage()

    auth_client = await AuthClientSingleton.get_instance()
    loop = asyncio.get_event_loop()
    task = loop.create_task(auth_client.start())

    yield
    # Cleanup resources
    # shutdown_storage()
    pass


app = FastAPI(title="AT_SIMULATION", version="1.0.0", lifespan=lifespan)
app.middleware("http")(cors_middleware)
app.middleware("http")(request_dump)
app.exception_handler(RequestValidationError)(validation_exception_handler)
