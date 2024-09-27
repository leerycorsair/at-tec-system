from abc import ABC, abstractmethod
from typing import List

from src.repository.editor.resource.models.models import ResourceDB, ResourceTypeDB


class IResourceRepository(ABC):
    @abstractmethod
    async def create_resource_type(self, resource_type: ResourceTypeDB) -> int:
        pass

    @abstractmethod
    async def get_resource_type(self, resource_type_id: int) -> ResourceTypeDB:
        pass

    @abstractmethod
    async def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]:
        pass

    @abstractmethod
    async def update_resource_type(self, resource_type: ResourceTypeDB) -> int:
        pass

    @abstractmethod
    async def delete_resource_type(self, resource_type_id: int) -> int:
        pass

    @abstractmethod
    async def create_resource(self, resource: ResourceDB) -> int:
        pass

    @abstractmethod
    async def get_resource(self, resource_id: int) -> ResourceDB:
        pass

    @abstractmethod
    async def get_resources(self, model_id: int) -> List[ResourceDB]:
        pass

    @abstractmethod
    async def update_resource(self, resource: ResourceDB) -> int:
        pass

    @abstractmethod
    async def delete_resource(self, resource_id: int) -> int:
        pass


class IVisioService(ABC):
    @abstractmethod
    async def create_node(
        self,
        object_id: int,
        object_type: str,
        model_id: int,
    ) -> int:
        pass

    @abstractmethod
    async def update_node(self, object_name: str, object_type: str) -> int:
        pass

    @abstractmethod
    async def delete_node(self, object_name: str, object_type: str) -> int:
        pass

    @abstractmethod
    async def create_edge(self, from_id: int, to_id: int) -> int:
        pass
