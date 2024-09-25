from typing import List, Optional
from pydantic import BaseModel


class FunctionParameterRequest(BaseModel):
    id: Optional[int] = None
    name: str
    type: str


class FunctionRequest(BaseModel):
    id: Optional[int] = None
    name: str
    ret_type: str
    body: str
    params: List[FunctionParameterRequest]


class FunctionParameterResponse(FunctionParameterRequest):
    id: int


class FunctionResponse(FunctionRequest):
    id: int
    params: List[FunctionParameterResponse]


class FunctionsResponse(BaseModel):
    functions: List[FunctionResponse]
    total: int
