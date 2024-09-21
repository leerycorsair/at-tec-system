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
