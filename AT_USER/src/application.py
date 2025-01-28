import asyncio
from contextlib import asynccontextmanager

from at_queue.core.session import ConnectionParameters
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.api import setup_routes
from src.config.rabbitmq import RabbitMQStore
from src.service.user.user import UserService
from src.worker.auth import AuthWorker


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_routes(app)

    rabbitmq_config = RabbitMQStore.get_rabbitmq_config()
    connection_parameters = ConnectionParameters(rabbitmq_config.url)

    user_service = UserService()
    auth_worker = AuthWorker(
        connection_parameters=connection_parameters, user_service=user_service
    )

    await auth_worker.initialize()
    await auth_worker.register()

    task = asyncio.create_task(auth_worker.start())

    try:
        yield
    finally:
        task.cancel()
        await auth_worker.stop()
        await auth_worker.close()


app = FastAPI(title="AT_USER", version="1.0.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
