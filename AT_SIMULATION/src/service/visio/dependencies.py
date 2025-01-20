from typing import List, Protocol

from fastapi import Depends

from src.repository.visio.models.models import (
    EdgeDB,
    EditorInfoDB,
    MoveNodeDB,
    NodeDB,
    NodeTablesEnum,
)
from src.repository.visio.repository import VisioRepository
from sqlalchemy.orm import Session
from src.storage.postgres.storage import get_db


class IVisioRepository(Protocol):
    def create_node(self, node: NodeDB) -> int: ...

    def update_node(self, node: NodeDB) -> int: ...

    def get_node(self, object_table: NodeTablesEnum, object_id: int) -> NodeDB: ...

    def get_node_by_id(self, node_id: int) -> NodeDB: ...

    def delete_node(self, object_table: NodeTablesEnum, object_id: int) -> int: ...

    def get_nodes(self, model_id: int) -> List[NodeDB]: ...

    def create_edge(self, edge: EdgeDB) -> int: ...

    def get_edges(self, model_id: int) -> List[EdgeDB]: ...

    def get_editor_info(self, model_id: int) -> EditorInfoDB: ...

    def move_node(self, params: MoveNodeDB) -> None: ...


def get_visio_repository(session: Session = Depends(get_db)) -> IVisioRepository:
    return VisioRepository(session)
