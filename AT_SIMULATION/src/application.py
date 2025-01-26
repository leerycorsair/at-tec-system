import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.client.auth_client import AuthClientSingleton
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_dump)
app.exception_handler(RequestValidationError)(validation_exception_handler)
