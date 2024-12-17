from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Union


class BaseTypesEnum(Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    BOOL = "BOOL"
    ENUM = "ENUM"


class ResourceTypeAttributeRequest(BaseModel):
    name: str
    type: BaseTypesEnum
    enum_values_set: Optional[List[str]] = None
    default_value: Optional[Union[int, float, bool, str]] = None


class ResourceTypeTypesEnum(Enum):
    CONSTANT = "CONSTANT"
    TEMPORAL = "TEMPORAL"


class ResourceTypeRequest(BaseModel):
    name: str
    type: ResourceTypeTypesEnum
    attributes: List[ResourceTypeAttributeRequest]


class ResourceAttributeRequest(BaseModel):
    rta_id: int
    value: str


class ResourceRequest(BaseModel):
    name: str
    to_be_traced: bool
    attributes: List[ResourceAttributeRequest]
    resource_type_id: int
