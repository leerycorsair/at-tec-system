from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ModelMetaDB(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: Optional[datetime] = None
