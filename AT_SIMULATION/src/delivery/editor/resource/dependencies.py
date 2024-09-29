from typing import List, Protocol

from src.repository.editor.resource.models.models import ResourceDB, ResourceTypeDB
from src.service.editor.resource.service import ResourceService


class IResourceService(Protocol):
    async def create_resource_type(self, resource_type: ResourceTypeDB) -> int: ...

    async def get_resource_type(
        self, resource_type_id: int, model_id: int
    ) -> ResourceTypeDB: ...

    async def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]: ...

    async def update_resource_type(self, resource_type: ResourceTypeDB) -> int: ...

    async def delete_resource_type(
        self, resource_type_id: int, model_id: int
    ) -> int: ...

    async def create_resource(self, resource: ResourceDB) -> int: ...

    async def get_resource(self, resource_id: int, model_id: int) -> ResourceDB: ...

    async def get_resources(self, model_id: int) -> List[ResourceDB]: ...

    async def update_resource(self, resource: ResourceDB) -> int: ...

    async def delete_resource(self, resource_id: int, model_id: int) -> int: ...


def get_resource_service() -> IResourceService:
    return ResourceService()
