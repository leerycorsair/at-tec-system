from typing import List, Protocol

from fastapi import Depends

from src.repository.editor.function.models.models import FunctionDB
from src.service.editor.function.dependencies import (get_function_repository,
                                                      get_visio_service)
from src.service.editor.function.service import FunctionService


class IFunctionService(Protocol):
    def create_function(self, function: FunctionDB) -> int: ...

    def get_function(self, function_id: int, model_id: int) -> FunctionDB: ...

    def get_functions(self, model_id: int) -> List[FunctionDB]: ...

    def update_function(self, function: FunctionDB) -> int: ...

    def delete_function(self, function_id: int, model_id: int) -> int: ...


def get_function_service(
    function_rep=Depends(get_function_repository),
    visio_service=Depends(get_visio_service),
) -> IFunctionService:
    return FunctionService(function_rep, visio_service)
