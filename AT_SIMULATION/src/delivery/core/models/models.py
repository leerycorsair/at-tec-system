from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class ObjectIDResponse(BaseModel):
    id: int


class CommonResponse(BaseModel, Generic[T]):
    status_code: int
    is_error: bool
    error_message: str
    data: Optional[T] = None

    class Config:
        orm_mode = True
        json_encoders = {None: lambda _: None}
