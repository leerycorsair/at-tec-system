from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class BaseTypesEnum(Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    ENUM = "enum"


class ResourceTypeAttrRequest(BaseModel):
    name: str
    type: BaseTypesEnum
    enum_values_set: Optional[List[str]] = None
    default_value: Optional[str] = None


class ResourceTypeRequest(BaseModel):
    name: str
    type: BaseTypesEnum
    attributes: List[ResourceTypeAttrRequest]


class ResourceTypeAttrResponse(BaseModel):
    id: int
    name: str
    type: BaseTypesEnum
    enum_values_set: Optional[List[str]] = None
    default_value: Optional[str] = None


class ResourceTypeResponse(BaseModel):
    id: int
    name: str
    type: BaseTypesEnum
    attributes: List[ResourceTypeAttrResponse]


class ResourceTypeTypesEnum(Enum):
    CONSTANT = "constant"
    TEMPORAL = "temporal"


class CreateResourceTypeRequest(ResourceTypeRequest):
    pass


class GetResourceTypeResponse(ResourceTypeResponse):
    pass


class GetResourceTypesResponse(BaseModel):
    resource_types: List[ResourceTypeResponse]
    total: int


class UpdateResourceTypeRequest(ResourceTypeRequest):
    id: int


class ResourceType(BaseModel):
    id: int
    name: str
    type: BaseTypesEnum
    attributes: List[ResourceTypeAttrRequest]
