from typing import List
from pydantic import BaseModel


class FunctionParameterRequest(BaseModel):
    name: str
    type: str


class FunctionRequest(BaseModel):
    name: str
    ret_type: str
    body: str
    params: List[FunctionParameterRequest]
