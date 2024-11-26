from typing import List

from src.repository.editor.resource.models.models import ResourceDB, ResourceTypeDB
from src.repository.visio.models.models import NodeTypesEnum
from src.service.editor.resource.dependencies import (
    IResourceRepository,
    IVisioService,
)
from src.service.helpers import handle_rollback


class ResourceService:
    def __init__(
        self,
        resource_rep: IResourceRepository,
        visio_service: IVisioService,
    ) -> None:
        self._resource_rep = resource_rep
        self._visio_service = visio_service

    def _check_resource_type_rights(self, resource_type_id: int, model_id: int) -> None:
        resource_type = self._resource_rep.get_resource_type(resource_type_id)
        if resource_type.model_id != model_id:
            raise ValueError(
                f"Resource type {resource_type_id} does not belong to model {model_id}"
            )

    def _check_resource_rights(
        self,
        resource_id: int,
        model_id: int,
    ) -> None:
        resource = self._resource_rep.get_resource(resource_id)
        if resource.model_id != model_id:
            raise ValueError(
                f"Resource {resource_id} does not belong to model {model_id}"
            )

    def create_resource_type(self, resource_type: ResourceTypeDB) -> int:
        obj_id = self._resource_rep.create_resource_type(resource_type)

        with handle_rollback(self._resource_rep.delete_resource_type, obj_id):
            self._visio_service.create_node(
                obj_id,
                resource_type.name,
                NodeTypesEnum.RESOURCE_TYPE,
                resource_type.model_id,
            )

        return obj_id

    def get_resource_type(self, resource_type_id: int, model_id: int) -> ResourceTypeDB:
        self._check_resource_type_rights(resource_type_id, model_id)
        return self._resource_rep.get_resource_type(resource_type_id)

    def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]:
        return self._resource_rep.get_resource_types(model_id)

    def update_resource_type(self, resource_type: ResourceTypeDB) -> int:
        self._check_resource_type_rights(resource_type.id, resource_type.model_id)
        original_resource_type = self._resource_rep.get_resource_type(resource_type.id)
        obj_id = self._resource_rep.update_resource_type(resource_type)

        with handle_rollback(
            self._resource_rep.update_resource_type, original_resource_type
        ):
            self._visio_service.update_node_name(
                obj_id, resource_type.name, NodeTypesEnum.RESOURCE_TYPE
            )

        return obj_id

    def delete_resource_type(self, resource_type_id: int, model_id: int) -> int:
        self._check_resource_type_rights(resource_type_id, model_id)
        return self._resource_rep.delete_resource_type(resource_type_id)

    def create_resource(self, resource: ResourceDB) -> int:
        obj_id = self._resource_rep.create_resource(resource)

        with handle_rollback(self._resource_rep.delete_resource, obj_id):
            resource_node_id = self._visio_service.create_node(
                obj_id,
                resource.name,
                NodeTypesEnum.RESOURCE,
                resource.model_id,
            )

        resource_type_node = self._visio_service.get_node(
            resource.resource_type_id, NodeTypesEnum.RESOURCE_TYPE
        )

        with handle_rollback(
            self._visio_service.delete_node, obj_id, NodeTypesEnum.RESOURCE
        ):
            with handle_rollback(self._resource_rep.delete_resource, obj_id):
                self._visio_service.create_edge(
                    resource_type_node.id, resource_node_id, resource.model_id
                )

        return obj_id

    def get_resource(self, resource_id: int, model_id: int) -> ResourceDB:
        self._check_resource_rights(resource_id, model_id)
        return self._resource_rep.get_resource(resource_id)

    def get_resources(self, model_id: int) -> List[ResourceDB]:
        return self._resource_rep.get_resources(model_id)

    def update_resource(self, resource: ResourceDB) -> int:
        self._check_resource_rights(resource.id, resource.model_id)
        original_resource = self._resource_rep.get_resource(resource.id)
        obj_id = self._resource_rep.update_resource(resource)

        with handle_rollback(self._resource_rep.update_resource, original_resource):
            self._visio_service.update_node_name(
                obj_id, resource.name, NodeTypesEnum.RESOURCE
            )

        return obj_id

    def delete_resource(self, resource_id: int, model_id: int) -> int:
        self._check_resource_rights(resource_id, model_id)
        return self._resource_rep.delete_resource(resource_id)
