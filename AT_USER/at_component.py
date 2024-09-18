from at_queue.core.at_component import ATComponent
from at_queue.utils.decorators import component_method
from at_queue.core.session import ConnectionParameters

from src.service.interface import UserServiceInterface
from src.service.user.user import UserService

from fastapi import Depends
import asyncio

class ATUserComponent(ATComponent):

    @component_method
    def verify_token(self, token: str):
        user_service = UserService()
        user_service.verify_token(token)


async def create_at_component():
    connection_parameters = ConnectionParameters('amqp://localhost:5672/')
    at_user_component = ATUserComponent(connection_parameters)
    await at_user_component.initialize()
    await at_user_component.register()
    await at_user_component.start()

if __name__ == '__main__':
    asyncio.run(create_at_component())

