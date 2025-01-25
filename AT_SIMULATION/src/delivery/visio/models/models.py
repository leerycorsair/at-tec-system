from enum import Enum
from typing import List

from pydantic import BaseModel


class NodeTypesEnum(str, Enum):
    RESOURCE = "RESOURCE"
    RESOURCE_TYPE = "RESOURCE_TYPE"
    FUNCTION = "FUNCTION"

    RULE_TEMPLATE = "RULE_TEMPLATE"
    RULE_USAGE = "RULE_USAGE"

    OPERATION_TEMPLATE = "OPERATION_TEMPLATE"
    OPERATION_USAGE = "OPERATION_USAGE"

    IRREGULAR_TEMPLATE = "IRREGULAR_TEMPLATE"
    IRREGULAR_USAGE = "IRREGULAR_USAGE"


class NodeResponse(BaseModel):
    id: int
    object_name: str
    node_type: NodeTypesEnum
    pos_x: int
    pos_y: int
    height: int
    width: int
    color: str


class EdgeResponse(BaseModel):
    id: int
    from_node: int
    to_node: int


class EditorInfoResponse(BaseModel):
    nodes: List[NodeResponse]
    edges: List[EdgeResponse]


class MoveNodeRequest(BaseModel):
    new_pos_x: int
    new_pos_y: int
