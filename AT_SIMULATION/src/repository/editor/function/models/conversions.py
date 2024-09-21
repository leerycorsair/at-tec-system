from typing import List
from src.repository.editor.function.models.models import FunctionDB, FunctionParameterDB
from src.schema.function import Function, FunctionParameter


def to_FunctionParameterDB(param: FunctionParameter) -> FunctionParameterDB:
    return FunctionParameterDB(
        id=param.id,
        name=param.name,
        type=param.type,
        function_id=param.function_id,
    )


def to_FunctionDB(func: Function, params: List[FunctionParameter]) -> FunctionDB:
    return FunctionDB(
        id=func.id,
        name=func.name,
        ret_type=func.ret_type,
        body=func.body,
        model_id=func.model_id,
        params=[to_FunctionParameterDB(param) for param in params],
    )


def to_Function(func: FunctionDB) -> Function:
    return Function(
        name=func.name,
        ret_type=func.ret_type,
        body=func.body,
        model_id=func.model_id,
    )


def to_FunctionParameter(param: FunctionParameterDB, func_id: int) -> FunctionParameter:
    return FunctionParameter(
        name=param.name,
        type=param.type,
        function_id=func_id,
    )
