from typing import List

from pydantic import BaseModel


class FunctionParameterDB(BaseModel):
    id: int
    name: str
    type: str
    function_id: int


class FunctionDB(BaseModel):
    id: int
    name: str
    ret_type: str
    body: str
    model_id: int
    params: List[FunctionParameterDB]
