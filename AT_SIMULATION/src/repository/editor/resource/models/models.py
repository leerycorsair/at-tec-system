from typing import List, Optional
from pydantic import BaseModel


class ResourceTypeAttributeDB(BaseModel):
    id: int
    name: str
    type: str
    default_value: Optional[str] = None
    resource_type_id: int


class ResourceTypeDB(BaseModel):
    id: int
    name: str
    type: str
    model_id: int
    attributes: List[ResourceTypeAttributeDB]


class ResourceAttrDB(BaseModel):
    id: str
    name: str
    value: str


class ResourceDB(BaseModel):
    id: int
    name: str
    type: str
    to_be_traced: bool
    attributes: List[ResourceAttrDB]
    model_id: int
