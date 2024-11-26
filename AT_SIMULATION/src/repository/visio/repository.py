from typing import List
from sqlalchemy.orm import Session


from src.repository.helper import handle_sqlalchemy_errors
from src.repository.visio.models.conversions import (
    to_Edge,
    to_EdgeDB,
    to_Node,
    to_NodeDB,
)
from src.repository.visio.models.models import EdgeDB, NodeDB, NodeTablesEnum
from src.schema.visio import Edge, Node
from src.storage.postgres.session import session_scope


class VisioRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @handle_sqlalchemy_errors
    def create_node(self, node: NodeDB) -> int:
        with session_scope(self.db_session) as session:
            new_node = to_Node(node)
            session.add(new_node)
            session.flush()

        return new_node.id

    @handle_sqlalchemy_errors
    def update_node(self, node: NodeDB) -> int:
        with session_scope(self.db_session) as session:
            existing_node = self._get_node(node.object_table, node.object_id)
            if not existing_node:
                raise RuntimeError("Node not found")
            existing_node.object_name = node.object_name
            existing_node.node_type = node.node_type
            existing_node.pos_x = node.pos_x
            existing_node.pos_y = node.pos_y
            existing_node.height = node.height
            existing_node.width = node.width
            existing_node.color = node.color
            session.commit()
        return existing_node.id

    @handle_sqlalchemy_errors
    def get_node(self, object_table: NodeTablesEnum, object_id: int) -> NodeDB:
        return to_NodeDB(self._get_node(object_table, object_id))

    @handle_sqlalchemy_errors
    def delete_node(self, object_table: NodeTablesEnum, object_id: int) -> int:
        with session_scope(self.db_session) as session:
            node = self._get_node(object_table, object_id)
            if not node:
                raise RuntimeError("Node not found")
            session.delete(node)
        return node.id

    @handle_sqlalchemy_errors
    def get_nodes(self, model_id: int) -> List[NodeDB]:
        nodes = self.db_session.query(Node).filter(Node.model_id == model_id).all()
        nodes_db = [to_NodeDB(node) for node in nodes]

        return nodes_db

    @handle_sqlalchemy_errors
    def create_edge(self, edge: EdgeDB) -> int:
        with session_scope(self.db_session) as session:
            new_edge = to_Edge(edge)
            session.add(new_edge)
            session.flush()
        return new_edge.id

    @handle_sqlalchemy_errors
    def get_edges(self, model_id: int) -> List[EdgeDB]:
        edges = self.db_session.query(Edge).filter(Edge.model_id == model_id).all()
        edges_db = [to_EdgeDB(edge) for edge in edges]

        return edges_db

    def _get_node(self, object_table: NodeTablesEnum, object_id: int) -> Node:
        node = (
            self.db_session.query(Node)
            .filter(Node.object_table == object_table and Node.object_id == object_id)
            .first()
        )
        if not node:
            raise ValueError("Node does not exist")
        return node
