from typing import List
from src.delivery.editor.function.models.models import (
    CreateFunctionRequest,
    CreateFunctionResponse,
    DeleteFunctionResponse,
    GetFunctionParameterResponse,
    GetFunctionResponse,
    GetFunctionsResponse,
    UpdateFunctionRequest,
    UpdateFunctionResponse,
    FunctionParameter,
)
from src.repository.editor.function.models.models import FunctionDB, FunctionParameterDB


def to_FunctionParameterDB(
    param: FunctionParameter,
    param_id: int,
    function_id: int,
) -> FunctionParameterDB:
    return FunctionParameterDB(
        id=param_id,
        name=param.name,
        type=param.type,
        function_id=function_id,
    )


def create_to_FunctionDB(
    function: CreateFunctionRequest,
    model_id: int,
) -> FunctionDB:
    return FunctionDB(
        id=0,
        name=function.name,
        ret_type=function.ret_type,
        body=function.body,
        model_id=model_id,
        params=[to_FunctionParameterDB(param, 0, 0) for param in function.params],
    )


def update_to_FunctionDB(
    function: UpdateFunctionRequest,
    model_id: int,
    function_id: int,
) -> FunctionDB:
    return FunctionDB(
        id=function_id,
        name=function.name,
        ret_type=function.ret_type,
        body=function.body,
        model_id=model_id,
        params=[
            to_FunctionParameterDB(param, param.id, function_id)
            for param in function.params
        ],
    )


def to_GetFuctionParameterResponse(
    param: FunctionParameterDB,
) -> GetFunctionParameterResponse:
    return GetFunctionParameterResponse(
        name=param.name,
        type=param.type,
        id=param.id,
    )


def to_GetFunctionResponse(function: FunctionDB) -> GetFunctionResponse:
    return GetFunctionResponse(
        name=function.name,
        ret_type=function.ret_type,
        body=function.body,
        params=[to_GetFuctionParameterResponse(param) for param in function.params],
        id=function.id,
    )


def to_GetFunctionsResponse(functions: List[FunctionDB]) -> GetFunctionsResponse:
    return GetFunctionsResponse(
        functions=[to_GetFunctionResponse(function) for function in functions],
        total=len(functions),
    )


def to_CreateFunctionResponse(function_id: int) -> CreateFunctionResponse:
    return CreateFunctionResponse(id=function_id)


def to_UpdateFunctionResponse(function_id: int) -> UpdateFunctionResponse:
    return UpdateFunctionResponse(id=function_id)


def to_DeleteFunctionResponse(function_id: int) -> DeleteFunctionResponse:
    return DeleteFunctionResponse(id=function_id)
