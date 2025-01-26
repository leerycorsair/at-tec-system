from src.core.errors import ForbiddenError
from src.repository.visio.models.conversions import to_NodeTablesEnum_from_node_type
from src.repository.visio.models.models import (
    EditorInfoDB,
    MoveNodeDB,
    NodeDB,
    NodeTypesEnum,
)
from src.service.visio.conversions import to_EdgeDB, to_NodeDB
from src.service.visio.dependencies import IVisioRepository


class VisioService:

    def __init__(
        self,
        visio_rep: IVisioRepository,
    ) -> None:
        self._visio_rep = visio_rep

    def _check_node_rights(self, node_id: int, model_id: int) -> None:
        node = self._visio_rep.get_node_by_id(node_id)
        if node.model_id != model_id:
            raise ForbiddenError(f"Node {node_id} does not belong to model {model_id}")

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

    def get_editor_info(self, model_id: int) -> EditorInfoDB:
        return self.get_editor_info(model_id)

    def move_node(self, params: MoveNodeDB, model_id: int) -> None:
        self._check_node_rights(params.node_id, model_id)
        return self.move_node(params, model_id)
