from typing import List
from src.repository.editor.resource.models.models import (
    ResourceAttributeDB,
    ResourceDB,
    ResourceTypeAttributeDB,
    ResourceTypeDB,
)
from src.schema.resource import (
    Resource,
    ResourceAttribute,
    ResourceType,
    ResourceTypeAttribute,
)


def to_ResourceType(resource_type: ResourceTypeDB) -> ResourceType:
    return ResourceType(
        name=resource_type.name,
        type=resource_type.type,
        model_id=resource_type.model_id,
    )


def to_ResourceTypeAttribute(
    attr: ResourceTypeAttributeDB, resource_type_id: int
) -> ResourceTypeAttribute:
    return ResourceTypeAttribute(
        name=attr.name,
        type=attr.type,
        default_value=attr.default_value,
        resource_type_id=resource_type_id,
    )


def to_ResourceTypeDB(
    resource_type: ResourceType, attrs: List[ResourceTypeAttribute]
) -> ResourceTypeDB:
    return ResourceTypeDB(
        id=resource_type.id,
        name=resource_type.name,
        type=resource_type.type,
        model_id=resource_type.model_id,
        attributes=[to_ResourceTypeAttributeDB(attr) for attr in attrs],
    )


def to_ResourceTypeAttributeDB(attr: ResourceTypeAttribute) -> ResourceTypeAttributeDB:
    return ResourceTypeAttributeDB(
        id=attr.id,
        name=attr.name,
        type=attr.type,
        default_value=attr.default_value,
        resource_type_id=attr.resource_type_id,
    )


def to_Resource(resource: ResourceDB) -> Resource:
    return Resource(
        name=resource.name,
        to_be_traced=resource.to_be_traced,
        resource_type_id=resource.resource_type_id,
        model_id=resource.model_id,
    )


def to_ResourceDB(
    resource: Resource, attributes: List[ResourceAttribute]
) -> ResourceDB:
    return ResourceDB(
        id=resource.id,
        name=resource.name,
        resource_type_id=resource.resource_type_id,
        to_be_traced=resource.to_be_traced,
        attributes=[to_ResourceAttributeDB(attr) for attr in attributes],
        model_id=resource.model_id,
    )


def to_ResourceAttribute(
    attr: ResourceAttributeDB, resource_id: int
) -> ResourceAttribute:
    return ResourceAttribute(
        value=attr.value,
        resource_id=resource_id,
        rta_id=attr.id,
    )


def to_ResourceAttributeDB(attr: ResourceAttribute) -> ResourceAttributeDB:
    return ResourceAttributeDB(
        id=attr.id,
        rta_id=attr.rta_id,
        value=attr.value,
        resource_id=attr.resource_id,
    )
