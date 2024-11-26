from typing import List, Protocol

from src.repository.editor.resource.models.models import ResourceDB, ResourceTypeDB
from src.repository.editor.resource.repository import ResourceRepository
from src.repository.visio.models.models import NodeDB, NodeTypesEnum
from src.service.visio.service import VisioService


class IResourceRepository(Protocol):
    def create_resource_type(self, resource_type: ResourceTypeDB) -> int: ...

    def get_resource_type(self, resource_type_id: int) -> ResourceTypeDB: ...

    def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]: ...

    def update_resource_type(self, resource_type: ResourceTypeDB) -> int: ...

    def delete_resource_type(self, resource_type_id: int) -> int: ...

    def create_resource(self, resource: ResourceDB) -> int: ...

    def get_resource(self, resource_id: int) -> ResourceDB: ...

    def get_resources(self, model_id: int) -> List[ResourceDB]: ...

    def update_resource(self, resource: ResourceDB) -> int: ...

    def delete_resource(self, resource_id: int) -> int: ...


def get_resource_repository() -> IResourceRepository:
    return ResourceRepository()


class IVisioService(Protocol):
    def create_node(
        self, object_id: int, object_name: str, node_type: NodeTypesEnum, model_id: int
    ) -> int: ...

    def update_node_name(
        self, object_id: int, object_name: str, node_type: NodeTypesEnum
    ) -> int: ...

    def get_node(self, object_id: int, node_type: NodeTypesEnum) -> NodeDB: ...

    def delete_node(self, object_id: int, node_type: NodeTypesEnum) -> int: ...

    def create_edge(self, from_id: int, to_id: int, model_id: int) -> int: ...


def get_visio_service() -> IVisioService:
    return VisioService()
