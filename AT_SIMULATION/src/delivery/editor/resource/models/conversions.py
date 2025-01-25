from typing import List

from src.delivery.editor.resource.models.models import (
    BaseTypesEnum,
    ResourceAttributeRequest,
    ResourceAttributeResponse,
    ResourceRequest,
    ResourceResponse,
    ResourcesResponse,
    ResourceTypeAttributeRequest,
    ResourceTypeAttributeResponse,
    ResourceTypeRequest,
    ResourceTypeResponse,
    ResourceTypesResponse,
    ResourceTypeTypesEnum,
)
from src.repository.editor.resource.models.models import (
    ResourceAttributeDB,
    ResourceDB,
    ResourceTypeAttributeDB,
    ResourceTypeDB,
)


def to_ResourceTypeAttributeDB(
    attr: ResourceTypeAttributeRequest,
    resource_type_id: int,
) -> ResourceTypeAttributeDB:
    return ResourceTypeAttributeDB(
        id=attr.id or 0,
        name=attr.name,
        type=attr.type.value,
        default_value=attr.default_value,
        enum_values_set=attr.enum_values_set,
        resource_type_id=resource_type_id,
    )


def to_ResourceTypeDB(
    request: ResourceTypeRequest,
    model_id: int,
) -> ResourceTypeDB:
    return ResourceTypeDB(
        id=request.id or 0,
        name=request.name,
        type=request.type.value,
        model_id=model_id,
        attributes=[
            to_ResourceTypeAttributeDB(attr, request.id or 0)
            for attr in request.attributes
        ],
    )


def to_ResourceTypeAttributeResponse(
    attr: ResourceTypeAttributeDB,
) -> ResourceTypeAttributeResponse:
    return ResourceTypeAttributeResponse(
        id=attr.id,
        name=attr.name,
        type=BaseTypesEnum(attr.type),
        enum_values_set=attr.enum_values_set,
        default_value=attr.default_value,
    )


def to_ResourceTypeResponse(
    resource_type: ResourceTypeDB,
) -> ResourceTypeResponse:
    return ResourceTypeResponse(
        id=resource_type.id,
        name=resource_type.name,
        type=ResourceTypeTypesEnum(resource_type.type),
        attributes=[
            to_ResourceTypeAttributeResponse(attr) for attr in resource_type.attributes
        ],
    )


def to_ResourceTypesResponse(
    resource_types: List[ResourceTypeDB],
) -> ResourceTypesResponse:
    return ResourceTypesResponse(
        resource_types=[
            to_ResourceTypeResponse(resource_type) for resource_type in resource_types
        ],
        total=len(resource_types),
    )


def to_ResourceAttributeDB(
    attr: ResourceAttributeRequest,
    resource_id: int,
) -> ResourceAttributeDB:
    return ResourceAttributeDB(
        id=attr.id or 0,
        rta_id=attr.rta_id,
        value=attr.value,
        resource_id=resource_id,
    )


def to_ResourceDB(
    request: ResourceRequest,
    model_id: int,
) -> ResourceDB:
    return ResourceDB(
        id=request.id or 0,
        name=request.name,
        to_be_traced=request.to_be_traced,
        attributes=[
            to_ResourceAttributeDB(attr, request.id or 0) for attr in request.attributes
        ],
        model_id=model_id,
        resource_type_id=request.resource_type_id,
    )


def to_ResourceAttributeResponse(
    attr: ResourceAttributeDB,
) -> ResourceAttributeResponse:
    return ResourceAttributeResponse(
        id=attr.id,
        rta_id=attr.rta_id,
        value=attr.value,
    )


def to_ResourceResponse(resource: ResourceDB) -> ResourceResponse:
    return ResourceResponse(
        name=resource.name,
        to_be_traced=resource.to_be_traced,
        attributes=[to_ResourceAttributeResponse(attr) for attr in resource.attributes],
        resource_type_id=resource.resource_type_id,
        id=resource.id,
    )


def to_ResourcesResponse(resources: List[ResourceDB]) -> ResourcesResponse:
    return ResourcesResponse(
        resources=[to_ResourceResponse(resource) for resource in resources],
        total=len(resources),
    )
