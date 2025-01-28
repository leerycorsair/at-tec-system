import asyncio
from contextlib import asynccontextmanager

from at_queue.core.session import ConnectionParameters
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.client.auth_client import AuthClientSingleton
from src.config.rabbitmq import RabbitMQStore
from src.delivery.core.middleware.fastapi_exception_handler import (
    validation_exception_handler,
)
from src.delivery.core.middleware.logging import LoggingMiddleware
from src.delivery.core.middleware.response import ResponseMiddleware
from src.providers.model import get_model_service
from src.providers.processor import get_processor_service
from src.providers.translator import get_translator_service
from src.worker.worker import ATSimulationWorker

from .delivery.router import setup_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_routes(app)
    # Initialize resources like database connections
    # setup_storage()

    auth_client = await AuthClientSingleton.get_instance()
    loop = asyncio.get_event_loop()
    task = loop.create_task(auth_client.start())

    rabbitmq_config = RabbitMQStore.get_rabbitmq_config()
    connection_parameters = ConnectionParameters(rabbitmq_config.url)
    simulation_worker = ATSimulationWorker(
        connection_parameters=connection_parameters,
        auth_client=auth_client,
        model_service=Depends(get_model_service),
        translator_service=Depends(get_translator_service),
        processor_service=Depends(get_processor_service),
    )

    await simulation_worker.initialize()
    await simulation_worker.register()

    task = asyncio.create_task(simulation_worker.start())

    try:
        yield
    finally:
        task.cancel()
        await simulation_worker.stop()
        await simulation_worker.close()

    # Cleanup resources
    # shutdown_storage()
    pass


app = FastAPI(title="AT_SIMULATION", version="1.0.0", lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ResponseMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.exception_handler(RequestValidationError)(validation_exception_handler)
