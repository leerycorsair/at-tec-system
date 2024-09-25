from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class BaseTypesEnum(Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    ENUM = "enum"


class ResourceTypeAttribute(BaseModel):
    name: str
    type: BaseTypesEnum
    enum_values_set: Optional[List[str]] = None
    default_value: Optional[str] = None


class ResourceTypeTypesEnum(Enum):
    CONSTANT = "constant"
    TEMPORAL = "temporal"


class ResourceType(BaseModel):
    name: str
    type: ResourceTypeTypesEnum
    attributes: List[ResourceTypeAttribute]


class CreateResourceTypeRequest(ResourceType):
    pass


class UpdateResourceTypeAttribute(ResourceTypeAttribute):
    id: int


class UpdateResourceTypeRequest(ResourceType):
    attributes: List[UpdateResourceTypeAttribute]


class GetResourceTypeResponse(ResourceType):
    id: int


class GetResourceTypesResponse(BaseModel):
    resource_types: List[GetResourceTypeResponse]
    total: int


class ResourceAttribute(BaseModel):
    rta_id: int
    value: str


class Resource(BaseModel):
    name: str
    to_be_traced: bool
    attributes: List[ResourceAttribute]
    resource_type_id: int


class CreateResourceRequest(Resource):
    pass


class UpdateResourceAttribute(ResourceAttribute):
    id: int


class UpdateResourceRequest(Resource):
    attributes: List[UpdateResourceAttribute]


class GetResourceResponse(Resource):
    id: int


class GetResourcesResponse(BaseModel):
    resources: List[GetResourceResponse]
    total: int
