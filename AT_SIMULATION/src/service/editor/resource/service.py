from typing import List
from fastapi import Depends

from src.repository.editor.resource.models.models import ResourceDB, ResourceTypeDB
from src.repository.editor.resource.repository import ResourceRepository
from src.service.editor.resource.dependencies import IResourceRepository, IVisioService


class ResourceService:
    def __init__(
        self,
        resource_rep: IResourceRepository = Depends(ResourceRepository),
        visio_service: IVisioService = Depends(),
    ) -> None:
        self._resource_rep = resource_rep
        self._visio_service = visio_service

    async def _check_resource_type_rights(
        self, resource_type_id: int, model_id: int
    ) -> None:
        resource_type = await self._resource_rep.get_resource_type(resource_type_id)
        if resource_type.model_id != model_id:
            raise ValueError(f"Resource type {resource_type_id} does not belong to model {model_id}")

    async def _handle_visio_operation(
        self, operation: str, name: str, entity_type: str, obj_id: int = None
    ) -> None:
        try:
            if operation == "create":
                await self._visio_service.create_node(obj_id, entity_type, name)
            elif operation == "update":
                await self._visio_service.update_node(name, entity_type)
            elif operation == "delete":
                await self._visio_service.delete_node(name, entity_type)
        except Exception as e:
            raise RuntimeError(f"Failed to {operation} visio node: {str(e)}")

    async def create_resource_type(self, resource_type: ResourceTypeDB) -> int:
        obj_id = await self._resource_rep.create_resource_type(resource_type)

        try:
            await self._handle_visio_operation(
                "create", resource_type.model_id, "resource_type", obj_id
            )
        except Exception as e:
            await self._resource_rep.delete_resource_type(obj_id)  
            raise e

        return obj_id

    async def get_resource_type(
        self, resource_type_id: int, model_id: int
    ) -> ResourceTypeDB:
        await self._check_resource_type_rights(resource_type_id, model_id)
        return await self._resource_rep.get_resource_type(resource_type_id)

    async def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]:
        return await self._resource_rep.get_resource_types(model_id)

    async def update_resource_type(self, resource_type: ResourceTypeDB) -> int:
        await self._check_resource_type_rights(resource_type.id, resource_type.model_id)
        original_resource_type = await self._resource_rep.get_resource_type(resource_type.id)
        obj_id = await self._resource_rep.update_resource_type(resource_type)

        try:
            await self._handle_visio_operation(
                "update", resource_type.name, "resource_type"
            )
        except Exception as e:
            await self._resource_rep.update_resource_type(original_resource_type)  
            raise e

        return obj_id

    async def delete_resource_type(self, resource_type_id: int, model_id: int) -> int:
        await self._check_resource_type_rights(resource_type_id, model_id)
        resource_type = await self._resource_rep.get_resource_type(resource_type_id)
        obj_id = await self._resource_rep.delete_resource_type(resource_type_id)

        try:
            await self._handle_visio_operation(
                "delete", resource_type.name, "resource_type"
            )
        except Exception as e:
            await self._resource_rep.create_resource_type(resource_type)  
            raise e

        return obj_id

    async def create_resource(self, resource: ResourceDB) -> int:
        pass

    async def get_resource(self, resource_id: int, model_id: int) -> ResourceDB:
        pass

    async def get_resources(self, model_id: int) -> List[ResourceDB]:
        pass

    async def update_resource(self, resource: ResourceDB) -> int:
        pass

    async def delete_resource(self, resource_id: int, model_id: int) -> int:
        pass
