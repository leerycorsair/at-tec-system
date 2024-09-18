import asyncio
from at_queue.core.at_component import ATComponent
from at_queue.core.session import ConnectionParameters
from at_queue.utils.decorators import component_method

from src.config.rabbitmq import RabbitMQStore


class AuthClient(ATComponent):
    @component_method
    async def verify_token(self, token: str) -> int:
        user_id = await self.exec_external_method(
            reciever="AuthWorker",
            methode_name="verify_token",
            method_args={"token": token},
        )
        return user_id  # type: ignore


class AuthClientSingleton:
    _instance = None

    @classmethod
    async def get_instance(cls) -> AuthClient:
        if cls._instance is None:
            rabbitmq_config = RabbitMQStore.get_rabbitmq_config()
            connection_parameters = ConnectionParameters(rabbitmq_config.url)
            cls._instance = AuthClient(connection_parameters)
            await cls._instance.initialize()
            await cls._instance.register()
        return cls._instance
