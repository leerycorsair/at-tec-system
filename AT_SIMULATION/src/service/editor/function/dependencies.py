from typing import List, Protocol

from fastapi import Depends

from sqlalchemy.orm import Session
from src.repository.editor.function.models.models import FunctionDB
from src.repository.editor.function.repository import FunctionRepository
from src.repository.visio.models.models import NodeTypesEnum
from src.service.visio.dependencies import get_visio_repository
from src.service.visio.service import VisioService
from src.storage.postgres.session import get_db


class IFunctionRepository(Protocol):
    def create_function(self, function: FunctionDB) -> int: ...

    def get_function(self, function_id: int) -> FunctionDB: ...

    def get_functions(self, model_id: int) -> List[FunctionDB]: ...

    def update_function(self, function: FunctionDB) -> int: ...

    def delete_function(self, function_id: int) -> int: ...


def get_function_repository(session: Session = Depends(get_db)) -> IFunctionRepository:
    return FunctionRepository(session)


class IVisioService(Protocol):
    def create_node(
        self, object_id: int, object_name: str, node_type: NodeTypesEnum, model_id: int
    ) -> int: ...

    def update_node_name(
        self, object_id: int, object_name: str, node_type: NodeTypesEnum
    ) -> int: ...


def get_visio_service(visio_rep=Depends(get_visio_repository)) -> IVisioService:
    return VisioService(visio_rep)
