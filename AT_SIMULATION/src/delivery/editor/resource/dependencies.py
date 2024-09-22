from abc import ABC, abstractmethod
from typing import List

from src.repository.editor.resource.models.models import ResourceDB, ResourceTypeDB
from src.service.editor.resource.service import ResourceService


class IResourceService(ABC):
    @abstractmethod
    async def create_resource_type(self, resource_type: ResourceTypeDB) -> int:
        pass

    @abstractmethod
    async def get_resource_type(
        self, resource_type_id: int, model_id: int
    ) -> ResourceTypeDB:
        pass

    @abstractmethod
    async def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]:
        pass

    @abstractmethod
    async def update_resource_type(self, resource_type: ResourceTypeDB) -> int:
        pass

    @abstractmethod
    async def delete_resource_type(self, resource_type_id: int, model_id: int) -> int:
        pass

    @abstractmethod
    async def create_resource(self, resource: ResourceDB) -> int:
        pass

    @abstractmethod
    async def get_resource(self, resource_id: int, model_id: int) -> ResourceDB:
        pass

    @abstractmethod
    async def get_resources(self, model_id: int) -> List[ResourceDB]:
        pass

    @abstractmethod
    async def update_resource(self, resource: ResourceDB) -> int:
        pass

    @abstractmethod
    async def delete_resource(self, resource_id: int, model_id: int) -> int:
        pass


def get_resource_service() -> IResourceService:
    return ResourceService()
