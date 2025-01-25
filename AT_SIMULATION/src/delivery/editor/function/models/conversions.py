from typing import List

from src.delivery.editor.function.models.models import (
    FunctionParameterRequest,
    FunctionParameterResponse,
    FunctionRequest,
    FunctionResponse,
    FunctionsResponse,
)
from src.repository.editor.function.models.models import FunctionDB, FunctionParameterDB


def to_FunctionParameterDB(
    param: FunctionParameterRequest,
    function_id: int,
) -> FunctionParameterDB:
    return FunctionParameterDB(
        id=param.id or 0,
        name=param.name,
        type=param.type,
        function_id=function_id,
    )


def to_FunctionDB(
    function: FunctionRequest,
    model_id: int,
) -> FunctionDB:
    return FunctionDB(
        id=function.id or 0,
        name=function.name,
        ret_type=function.ret_type,
        body=function.body,
        model_id=model_id,
        params=[
            to_FunctionParameterDB(param, function.id or 0) for param in function.params
        ],
    )


def to_FunctionParameterResponse(
    param: FunctionParameterDB,
) -> FunctionParameterResponse:
    return FunctionParameterResponse(
        name=param.name,
        type=param.type,
        id=param.id,
    )


def to_FunctionResponse(function: FunctionDB) -> FunctionResponse:
    return FunctionResponse(
        name=function.name,
        ret_type=function.ret_type,
        body=function.body,
        params=[to_FunctionParameterResponse(param) for param in function.params],
        id=function.id,
    )


def to_FunctionsResponse(functions: List[FunctionDB]) -> FunctionsResponse:
    return FunctionsResponse(
        functions=[to_FunctionResponse(function) for function in functions],
        total=len(functions),
    )
