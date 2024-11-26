from typing import Optional
from src.repository.visio.models.conversions import to_NodeTablesEnum_from_node_type
from src.repository.visio.models.models import EdgeDB, NodeDB, NodeTypesEnum

DEFAULT_NODE_X = 0
DEFAULT_NODE_Y = 0
DEFAULT_NODE_HEIGHT = 100
DEFAULT_NODE_WIDTH = 200

COLOR_RESOURCE_TYPE = "#28e302"
COLOR_RESOURCE = "#1c9903"
COLOR_FUNCTION = "#a603a3"
COLOR_IRREGULAR_EVENT_T = "#d4446f"
COLOR_IRREGULAR_EVENT_U = "#a33455"
COLOR_OPERATION_T = "#5047d6"
COLOR_OPERATION_U = "#302b82"
COLOR_RULE_T = "#e3e639"
COLOR_RULE_U = "#b5b82e"

_colors = {
    NodeTypesEnum.RESOURCE_TYPE: COLOR_RESOURCE_TYPE,
    NodeTypesEnum.RESOURCE: COLOR_RESOURCE,
    NodeTypesEnum.FUNCTION: COLOR_FUNCTION,
    NodeTypesEnum.IRREGULAR_EVENT_T: COLOR_IRREGULAR_EVENT_T,
    NodeTypesEnum.IRREGULAR_EVENT_U: COLOR_IRREGULAR_EVENT_U,
    NodeTypesEnum.OPERATION_T: COLOR_OPERATION_T,
    NodeTypesEnum.OPERATION_U: COLOR_OPERATION_U,
    NodeTypesEnum.RULE_T: COLOR_RULE_T,
    NodeTypesEnum.RULE_U: COLOR_RULE_U,
}


def to_NodeDB(
    object_id: int,
    object_name: str,
    node_type: NodeTypesEnum,
    model_id: Optional[int] = 0,
) -> NodeDB:
    return NodeDB(
        id=0,
        object_table=to_NodeTablesEnum_from_node_type(node_type),
        object_name=object_name,
        object_id=object_id,
        node_type=node_type,
        pos_x=DEFAULT_NODE_X,
        pos_y=DEFAULT_NODE_Y,
        height=DEFAULT_NODE_HEIGHT,
        width=DEFAULT_NODE_WIDTH,
        color=_colors.get(node_type),
        model_id=model_id or 0,
    )


def to_EdgeDB(from_id: int, to_id: int, model_id: int) -> EdgeDB:
    return to_EdgeDB(
        from_id=from_id,
        to_id=to_id,
        model_id=model_id,
    )
