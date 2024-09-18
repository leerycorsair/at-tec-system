from at_queue.core.at_component import ATComponent
from at_queue.utils.decorators import component_method

from src.service.user.user import UserService


class AuthWorker(ATComponent):
    def __init__(self, connection_parameters, user_service: UserService):
        super().__init__(connection_parameters=connection_parameters)
        self.user_service = user_service

    @component_method
    def verify_token(self, token: str) -> int:
        return self.user_service.verify_token(token)
