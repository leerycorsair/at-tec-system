from src.delivery.visio.models.models import (EdgeResponse, EditorInfoResponse,
                                              MoveNodeRequest, NodeResponse,
                                              NodeTypesEnum)
from src.repository.visio.models.models import (EdgeDB, EditorInfoDB,
                                                MoveNodeDB, NodeDB)


def to_MoveNodeDB(params: MoveNodeRequest, node_id: int) -> MoveNodeDB:
    return MoveNodeDB(
        node_id=node_id,
        new_pos_x=params.new_pos_x,
        new_pos_y=params.new_pos_y,
    )


def to_NodeResponse(node: NodeDB) -> NodeResponse:
    return NodeResponse(
        id=node.id,
        object_name=node.object_name,
        node_type=NodeTypesEnum(node.node_type),
        pos_x=node.pos_x,
        pos_y=node.pos_y,
        height=node.height,
        width=node.width,
        color=node.color,
    )


def to_EdgeResponse(edge: EdgeDB) -> EdgeResponse:
    return EdgeResponse(
        id=edge.id,
        from_node=edge.from_node,
        to_node=edge.from_node,
    )


def to_EditorInfoResponse(info: EditorInfoDB) -> EditorInfoResponse:
    return EditorInfoResponse(
        nodes=[to_NodeResponse(node) for node in info.nodes],
        edges=[to_EdgeResponse(edge) for edge in info.edges],
    )
