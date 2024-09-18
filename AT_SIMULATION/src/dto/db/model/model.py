from datetime import datetime
from pydantic import BaseModel


class CreateModelParamsDB(BaseModel):
    name: str
    user_id: str


class ModelMetaDB(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime


class UpdateModelParamsDB(BaseModel):
    name: str
