from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ModelMetaRequest(BaseModel):
    id: Optional[int] = None
    name: str


class ModelMetaResponse(ModelMetaRequest):
    id: int
    created_at: datetime


class ModelMetasResponse(BaseModel):
    metas: List[ModelMetaResponse]
    total: int
