from typing import List
from fastapi import Depends
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
from src.store.postgres.session import get_db


class VisioRepository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db_session = db_session

    @handle_sqlalchemy_errors
    def create_node(self, node: NodeDB) -> int:
        with self.db_session.begin():
            new_node = to_Node(node)
            self.db_session.add(new_node)
            self.db_session.flush()

        return new_node.id

    @handle_sqlalchemy_errors
    def update_node(self, node: NodeDB) -> int:
        with self.db_session.begin():
            existing_node = self._get_node_by_id(node.id)
            if not existing_node:
                raise RuntimeError("Node not found")

            existing_node.object_name = node.object_name
            existing_node.node_type = node.node_type
            existing_node.pos_x = node.pos_x
            existing_node.pos_y = node.pos_y
            existing_node.height = node.height
            existing_node.width = node.width
            existing_node.color = node.color

        return existing_node.id

    @handle_sqlalchemy_errors
    def get_node_by_id(self, node_id: int) -> NodeDB:
        return to_NodeDB(self._get_node_by_id(node_id))

    @handle_sqlalchemy_errors
    def get_node_by_obj(self, object_table: NodeTablesEnum, object_id: int) -> NodeDB:
        return to_NodeDB(self._get_node_by_obj(object_table, object_id))

    @handle_sqlalchemy_errors
    def delete_node(self, object_table: NodeTablesEnum, object_id: int) -> int:
        with self.db_session.begin():
            node = self._get_node_by_obj(object_table, object_id)
            if not node:
                raise RuntimeError("Node not found")

            self.db_session.delete(node)
        return node.id

    @handle_sqlalchemy_errors
    def get_nodes(self, model_id: int) -> List[NodeDB]:
        nodes = self.db_session.query(Node).filter(Node.model_id == model_id).all()
        nodes_db = [to_NodeDB(node) for node in nodes]

        return nodes_db

    @handle_sqlalchemy_errors
    def create_edge(self, edge: EdgeDB) -> int:
        with self.db_session.begin():
            new_edge = to_Edge(edge)
            self.db_session.add(new_edge)
            self.db_session.flush()
        return new_edge.id

    @handle_sqlalchemy_errors
    def get_edges(self, model_id: int) -> List[EdgeDB]:
        edges = self.db_session.query(Edge).filter(Edge.model_id == model_id).all()
        edges_db = [to_EdgeDB(edge) for edge in edges]

        return edges_db

    def _get_node_by_id(self, node_id: int) -> Node:
        return self.db_session.query(Node).filter(Node.id == node_id).first()

    def _get_node_by_obj(self, object_table: NodeTablesEnum, object_id: int) -> Node:
        return (
            self.db_session.query(Node)
            .filter(Node.object_table == object_table and Node.object_id == object_id)
            .first()
        )
