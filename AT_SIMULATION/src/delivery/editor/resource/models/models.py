from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class BaseTypesEnum(Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    ENUM = "enum"


class ResourceTypeAttributeRequest(BaseModel):
    id: Optional[int] = None
    name: str
    type: BaseTypesEnum
    enum_values_set: Optional[List[str]] = None
    default_value: Optional[str] = None


class ResourceTypeAttributeResponse(ResourceTypeAttributeRequest):
    id: int


class ResourceTypeTypesEnum(Enum):
    CONSTANT = "constant"
    TEMPORAL = "temporal"


class ResourceTypeRequest(BaseModel):
    id: Optional[int] = None
    name: str
    type: ResourceTypeTypesEnum
    attributes: List[ResourceTypeAttributeRequest]


class ResourceTypeResponse(ResourceTypeRequest):
    id: int
    attributes: List[ResourceTypeAttributeResponse]


class ResourceTypesResponse(BaseModel):
    resource_types: List[ResourceTypeResponse]
    total: int


class ResourceAttributeRequest(BaseModel):
    id: Optional[int] = None
    rta_id: int
    value: str


class ResourceAttributeResponse(ResourceAttributeRequest):
    id: int


class ResourceRequest(BaseModel):
    id: Optional[int] = None
    name: str
    to_be_traced: bool
    attributes: List[ResourceAttributeRequest]
    resource_type_id: int


class ResourceResponse(ResourceRequest):
    id: int
    attributes: List[ResourceAttributeResponse]


class ResourcesResponse(BaseModel):
    resources: List[ResourceResponse]
    total: int
