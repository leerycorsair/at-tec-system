from fastapi import Depends
from src.repository.visio.models.conversions import to_NodeTablesEnum_from_node_type
from src.repository.visio.models.models import NodeDB, NodeTypesEnum
from src.service.visio.conversions import to_EdgeDB, to_NodeDB
from src.service.visio.dependencies import IVisioRepository, get_visio_repository


class VisioService:

    def __init__(
        self,
        visio_rep: IVisioRepository = Depends(get_visio_repository),
    ) -> None:
        self._visio_rep = visio_rep

    def create_node(
        self, object_id: int, object_name: str, node_type: NodeTypesEnum, model_id: int
    ) -> int:
        node = to_NodeDB(object_id, object_name, node_type, model_id)
        return self._visio_rep.create_node(node)

    def update_node_name(
        self, object_id: int, object_name: str, node_type: NodeTypesEnum
    ) -> int:
        node = to_NodeDB(object_id, object_name, node_type)
        return self._visio_rep.update_node(node)

    def get_node(self, object_id: int, node_type: NodeTypesEnum) -> NodeDB:
        return self._visio_rep.get_node(
            to_NodeTablesEnum_from_node_type(node_type), object_id
        )

    def delete_node(self, object_id: int, node_type: NodeTypesEnum) -> int:
        return self._visio_rep.delete_node(
            to_NodeTablesEnum_from_node_type(node_type), object_id
        )

    def create_edge(self, from_id: int, to_id: int, model_id: int) -> int:
        edge = to_EdgeDB(from_id, to_id, model_id)
        return self._visio_rep.create_edge(edge)
