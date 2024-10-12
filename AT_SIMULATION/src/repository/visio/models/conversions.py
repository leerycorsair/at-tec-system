from src.repository.visio.models.models import EdgeDB, NodeDB
from src.schema.visio import Edge, Node


def to_Node(node: NodeDB) -> Node:
    return Node(
        object_table=node.object_table,
        object_name=node.object_name,
        object_id=node.object_id,
        node_type=node.node_type,
        pos_x=node.pos_x,
        pos_y=node.pos_y,
        width=node.width,
        height=node.height,
        color=node.color,
        model_id=node.model_id,
    )


def to_NodeDB(node: Node) -> NodeDB:
    return NodeDB(
        id=node.id,
        object_table=node.object_table,
        object_name=node.object_name,
        object_id=node.object_id,
        node_type=node.node_type,
        pos_x=node.pos_x,
        pos_y=node.pos_y,
        width=node.width,
        height=node.height,
        color=node.color,
        model_id=node.model_id,
    )


def to_Edge(edge: EdgeDB) -> Edge:
    return Edge(
        from_node=edge.from_node,
        no_node=edge.to_node,
        model_id=edge.model_id,
    )


def to_EdgeDB(edge: Edge) -> EdgeDB:
    return EdgeDB(
        id=edge.id,
        from_node=edge.from_node,
        to_node=edge.to_node,
        model_id=edge.model_id,
    )
