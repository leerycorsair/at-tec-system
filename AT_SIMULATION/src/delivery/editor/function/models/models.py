from typing import List
from pydantic import BaseModel


class FunctionParameter(BaseModel):
    name: str
    type: str


class Function(BaseModel):
    name: str
    ret_type: str
    body: str
    params: List[FunctionParameter]


class CreateFunctionRequest(Function):
    pass


class CreateFunctionResponse(BaseModel):
    id: int


class UpdateFunctionParameterRequest(FunctionParameter):
    id: int


class UpdateFunctionRequest(Function):
    params: List[UpdateFunctionParameterRequest]


class UpdateFunctionResponse(BaseModel):
    id: int


class GetFunctionParameterResponse(FunctionParameter):
    id: int


class GetFunctionResponse(Function):
    id: int
    params: List[GetFunctionParameterResponse]


class GetFunctionsResponse(BaseModel):
    functions: List[GetFunctionResponse]
    total: int


class DeleteFunctionResponse(BaseModel):
    id: int
