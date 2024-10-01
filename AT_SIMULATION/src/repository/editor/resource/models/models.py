from typing import List, Optional, Union
from pydantic import BaseModel


class ResourceTypeAttributeDB(BaseModel):
    id: int
    name: str
    type: str
    default_value: Optional[Union[int, float, bool, str]] = None
    enum_values_set: Optional[List[str]] = None
    resource_type_id: int


class ResourceTypeDB(BaseModel):
    id: int
    name: str
    type: str
    model_id: int
    attributes: List[ResourceTypeAttributeDB]


class ResourceAttributeDB(BaseModel):
    id: int
    rta_id: int
    resource_id: int
    value: str


class ResourceDB(BaseModel):
    id: int
    name: str
    to_be_traced: bool
    attributes: List[ResourceAttributeDB]
    model_id: int
    resource_type_id: int
