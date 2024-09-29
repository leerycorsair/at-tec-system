from typing import List, Protocol

from src.repository.editor.function.models.models import FunctionDB
from src.repository.editor.function.repository import FunctionRepository
from src.service.visio.service import VisioService


class IFunctionRepository(Protocol):
    def create_function(self, function: FunctionDB) -> int: ...

    def get_function(self, function_id: int) -> FunctionDB: ...

    def get_functions(self, model_id: int) -> List[FunctionDB]: ...

    def update_function(self, function: FunctionDB) -> int: ...

    def delete_function(self, function_id: int) -> int: ...

def get_function_repository()-> IFunctionRepository:
    return FunctionRepository()

class IVisioService(Protocol):
    def create_node(
        self,
        object_id: int,
        object_type: str,
        object_name: str,
        model_id: int,
    ) -> int: ...

    def update_node(
        self,
        object_id: int,
        object_type: str,
        object_name: str,
    ) -> None: ...

    def get_node_id(self, object_id: int, object_type: str) -> int: ...

    def delete_node(
        self,
        object_id: int,
        object_type: str,
    ) -> None: ...

    def create_edge(
        self,
        from_id: int,
        to_id: int,
        model_id: int,
    ) -> None: ...


def get_visio_service() -> IVisioService:
    return VisioService()
