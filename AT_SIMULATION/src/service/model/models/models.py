from datetime import datetime
from typing import List
from pydantic import BaseModel

from src.service.visio.models.models import Edge, Node


class ModelMeta(BaseModel):
    id: int
    name: str
    created_at: datetime
