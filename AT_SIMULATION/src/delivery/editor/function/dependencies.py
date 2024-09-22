from abc import ABC, abstractmethod
from typing import List
from src.repository.editor.function.models.models import FunctionDB
from src.service.editor.function.service import FunctionService


class IFunctionService(ABC):
    @abstractmethod
    async def create_function(self, function: FunctionDB) -> int:
        pass

    @abstractmethod
    async def get_function(self, function_id: int, model_id: int) -> FunctionDB:
        pass

    @abstractmethod
    async def get_functions(self, model_id: int) -> List[FunctionDB]:
        pass

    @abstractmethod
    async def update_function(self, function: FunctionDB) -> int:
        pass

    @abstractmethod
    async def delete_function(self, function_id: int, model_id: int) -> int:
        pass


def get_function_service() -> IFunctionService:
    return FunctionService()
