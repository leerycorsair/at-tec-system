from fastapi import Depends, HTTPException
from src.dto.api.editor.resource import (
    CreateResourceTypeRequest,
    GetResourceTypeResponse,
    GetResourceTypesResponse,
    UpdateResourceTypeRequest,
)
from src.dto.db.editor.resource import ResourceTypeDB
from src.repository.editor.resource.repository import ResourceRepository


def map_resource_type_db_to_response(
    resource_type_db: ResourceTypeDB,
) -> GetResourceTypeResponse:
    return GetResourceTypeResponse(
        id=resource_type_db.id,
        name=resource_type_db.name,
        type=resource_type_db.type,
        model_id=resource_type_db.model_id,
        attributes=resource_type_db.attributes,
    )


def map_resource_types_db_to_response(
    resource_types: list[ResourceTypeDB],
) -> GetResourceTypesResponse:
    return GetResourceTypesResponse(
        resource_types=[
            map_resource_type_db_to_response(resource_type)
            for resource_type in resource_types
        ],
        total=len(resource_types),
    )


class ResourceService:
    def __init__(
        self,
        resource_rep: ResourceRepository = Depends(ResourceRepository),
    ) -> None:
        self._resource_rep = resource_rep

    async def _check_resource_type_rights(
        self, resource_type_id: int, model_id: int
    ) -> bool:
        resource_type = await self._resource_rep.get_resource_type(resource_type_id)
        return resource_type.model_id == model_id

    async def create_resource_type(
        self,
        resource_type: CreateResourceTypeRequest,
        model_id: int
    ) -> int:
        resource_type_db = ResourceTypeDB(
            name=resource_type.name,
            type=resource_type.type,
            model_id=model_id,
            attributes=resource_type.attributes,
        )
        return await self._resource_rep.create_resource_type(resource_type_db)

    async def get_resource_type(
        self, resource_type_id: int, model_id: int
    ) -> GetResourceTypeResponse:
        if not await self._check_resource_type_rights(resource_type_id, model_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        resource_type_db = await self._resource_rep.get_resource_type(resource_type_id)
        return map_resource_type_db_to_response(resource_type_db)

    async def get_resource_types(self, model_id: int) -> GetResourceTypesResponse:
        resource_types = await self._resource_rep.get_resource_types(model_id)
        return map_resource_types_db_to_response(resource_types)

    async def update_resource_type(
        self, resource_type: UpdateResourceTypeRequest, model_id: int
    ) -> None:
        if not await self._check_resource_type_rights(resource_type.id, model_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        await self._resource_rep.update_resource_type(resource_type)

    async def delete_resource_type(self, resource_type_id: int, model_id: int) -> None:
        if not await self._check_resource_type_rights(resource_type_id, model_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        await self._resource_rep.delete_resource_type(resource_type_id)
