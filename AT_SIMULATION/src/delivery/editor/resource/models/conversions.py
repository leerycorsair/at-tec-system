from typing import List
from src.delivery.editor.resource.models.models import (
    BaseTypesEnum,
    CreateResourceRequest,
    CreateResourceResponse,
    CreateResourceTypeRequest,
    CreateResourceTypeResponse,
    DeleteResourceResponse,
    DeleteResourceTypeResponse,
    GetResourceResponse,
    GetResourceTypeResponse,
    GetResourceTypesResponse,
    GetResourcesResponse,
    Resource,
    ResourceAttribute,
    ResourceTypeAttribute,
    ResourceTypeTypesEnum,
    UpdateResourceRequest,
    UpdateResourceResponse,
    UpdateResourceTypeRequest,
    UpdateResourceTypeResponse,
)
from src.repository.editor.resource.models.models import (
    ResourceAttributeDB,
    ResourceDB,
    ResourceTypeAttributeDB,
    ResourceTypeDB,
)


def to_ResourceTypeAttributeDB(
    attr: ResourceTypeAttribute,
    resource_type_id: int,
    attr_id: int,
) -> ResourceTypeAttributeDB:
    return ResourceTypeAttributeDB(
        id=attr_id,
        name=attr.name,
        type=attr.type.value,
        default_value=attr.default_value,
        enum_values_set=attr.enum_values_set,
        resource_type_id=resource_type_id,
    )


def to_CreateResourceTypeResponse(
    resource_type_id: int,
) -> CreateResourceTypeResponse:
    return CreateResourceTypeResponse(id=resource_type_id)


def create_to_ResourceTypeDB(
    request: CreateResourceTypeRequest,
    model_id: int,
) -> ResourceTypeDB:
    return ResourceTypeDB(
        id=0,
        name=request.name,
        type=request.type.value,
        model_id=model_id,
        attributes=[
            to_ResourceTypeAttributeDB(attr, 0, 0) for attr in request.attributes
        ],
    )


def update_to_ResourceTypeDB(
    request: UpdateResourceTypeRequest,
    model_id: int,
    resource_type_id: int,
) -> ResourceTypeDB:
    return ResourceTypeDB(
        id=resource_type_id,
        name=request.name,
        type=request.type.value,
        model_id=model_id,
        attributes=[
            to_ResourceTypeAttributeDB(attr, resource_type_id, attr.id)
            for attr in request.attributes
        ],
    )


def to_ResourceTypeAttribute(attr: ResourceTypeAttributeDB) -> ResourceTypeAttribute:
    return ResourceTypeAttribute(
        name=attr.name,
        type=BaseTypesEnum(attr.type),
        enum_values_set=attr.enum_values_set,
        default_value=attr.default_value,
    )


def to_GetResourceTypeResponse(
    resource_type: ResourceTypeDB,
) -> GetResourceTypeResponse:
    return GetResourceTypeResponse(
        name=resource_type.name,
        type=ResourceTypeTypesEnum(resource_type.type),
        attributes=[
            to_ResourceTypeAttribute(attr) for attr in resource_type.attributes
        ],
        id=resource_type.id,
    )


def to_GetResourceTypesResponse(
    resource_types: List[ResourceTypeDB],
) -> GetResourceTypesResponse:
    return GetResourceTypesResponse(
        resource_types=[
            to_GetResourceTypeResponse(resource_type)
            for resource_type in resource_types
        ],
        total=len(resource_types),
    )


def to_UpdateResourceTypeResponse(
    resource_type_id: int,
) -> UpdateResourceTypeResponse:
    return UpdateResourceTypeResponse(id=resource_type_id)


def to_DeleteResourceTypeResponse(
    resource_type_id: int,
) -> DeleteResourceTypeResponse:
    return DeleteResourceTypeResponse(id=resource_type_id)


def to_ResourceAttributeDB(
    attr: ResourceAttribute,
    resource_id: int,
    attr_id: int,
) -> ResourceAttributeDB:
    return ResourceAttributeDB(
        id=attr_id,
        rta_id=attr.rta_id,
        value=attr.value,
        resource_id=resource_id,
    )


def create_to_ResourceDB(
    request: CreateResourceRequest,
    model_id: int,
) -> ResourceDB:
    return ResourceDB(
        id=0,
        name=request.name,
        to_be_traced=request.to_be_traced,
        attributes=[to_ResourceAttributeDB(attr, 0, 0) for attr in request.attributes],
        model_id=model_id,
        resource_type_id=request.resource_type_id,
    )


def update_to_ResourceDB(
    request: UpdateResourceRequest,
    model_id: int,
    resource_id: int,
) -> ResourceDB:
    return ResourceDB(
        id=resource_id,
        name=request.name,
        to_be_traced=request.to_be_traced,
        attributes=[
            to_ResourceAttributeDB(attr, resource_id, attr.id)
            for attr in request.attributes
        ],
        model_id=model_id,
        resource_type_id=request.resource_type_id,
    )


def to_CreateResourceResponse(
    resource_id: int,
) -> CreateResourceResponse:
    return CreateResourceResponse(id=resource_id)


def to_UpdateResourceResponse(
    resource_id: int,
) -> UpdateResourceResponse:
    return UpdateResourceResponse(id=resource_id)


def to_DeleteResourceResponse(
    resource_id: int,
) -> DeleteResourceResponse:
    return DeleteResourceResponse(id=resource_id)


def to_ResourceAttribute(attr: ResourceAttributeDB) -> ResourceAttribute:
    return ResourceAttribute(
        rta_id=attr.rta_id,
        value=attr.value,
    )


def to_GetResourceResponse(resource: ResourceDB) -> GetResourceResponse:
    return GetResourceResponse(
        name=resource.name,
        to_be_traced=resource.to_be_traced,
        attributes=[to_ResourceAttribute(attr) for attr in resource.attributes],
        resource_type_id=resource.resource_type_id,
        id=resource.id,
    )


def to_GetResourcesResponse(resources: List[ResourceDB]) -> GetResourcesResponse:
    return GetResourcesResponse(
        resources=[to_GetResourceResponse(resource) for resource in resources],
        total=len(resources),
    )
