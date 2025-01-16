from enum import Enum
from typing import List
from pydantic import BaseModel

from src.schema.function import Function
from src.schema.resource import Resource, ResourceType
from src.schema.template import Template, TemplateUsage


class NodeTablesEnum(Enum):
    RESOURCE_TYPE = ResourceType
    RESOURCE = Resource
    FUNCTION = Function
    TEMPLATE = Template
    TEMPLATE_USAGE = TemplateUsage


class NodeTypesEnum(str, Enum):
    RESOURCE_TYPE = "RESOURCE_TYPE"
    RESOURCE = "RESOURCE"
    FUNCTION = "FUNCTION"
    IRREGULAR_EVENT_U = "IRREGULAR_USAGE"
    IRREGULAR_EVENT_T = "IRREGULAR_TEMPLATE"
    OPERATION_U = "OPERATION_USAGE"
    OPERATION_T = "OPERATION_TEMPLATE"
    RULE_U = "RULE_USAGE"
    RULE_T = "RULE_TEMPLATE"


class NodeDB(BaseModel):
    id: int
    object_table: NodeTablesEnum
    object_name: str
    object_id: int
    node_type: NodeTypesEnum
    pos_x: int
    pos_y: int
    height: int
    width: int
    color: str
    model_id: int


class EdgeDB(BaseModel):
    id: int
    from_node: int
    to_node: int
    model_id: int


class MoveNodeDB(BaseModel):
    node_id: int
    new_pos_x: int
    new_pos_y: int


class EditorInfoDB(BaseModel):
    nodes: List[NodeDB]
    edges: List[EdgeDB]
