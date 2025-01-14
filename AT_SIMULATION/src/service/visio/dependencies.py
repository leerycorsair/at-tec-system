from typing import List, Protocol

from fastapi import Depends

from src.repository.visio.models.models import EdgeDB, NodeDB, NodeTablesEnum
from src.repository.visio.repository import VisioRepository
from sqlalchemy.orm import Session

from src.storage.postgres.session import get_db


class IVisioRepository(Protocol):
    def create_node(self, node: NodeDB) -> int: ...

    def update_node(self, node: NodeDB) -> int: ...

    def get_node(self, object_table: NodeTablesEnum, object_id: int) -> NodeDB: ...

    def delete_node(self, object_table: NodeTablesEnum, object_id: int) -> int: ...

    def get_nodes(self, model_id: int) -> List[NodeDB]: ...

    def create_edge(self, edge: EdgeDB) -> int: ...

    def get_edges(self, model_id: int) -> List[EdgeDB]: ...


def get_visio_repository(session: Session = Depends(get_db)) -> IVisioRepository:
    return VisioRepository(session)
