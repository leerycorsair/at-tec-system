from enum import Enum
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
    RESOURCE_TYPE = "resource_type"
    RESOURCE = "resource"
    FUNCTION = "function"
    IRREGULAR_EVENT_U = "irregular_event_usage"
    IRREGULAR_EVENT_T = "irregular_event_template"
    OPERATION_U = "operation_usage"
    OPERATION_T = "operation_template"
    RULE_U = "rule_usage"
    RULE_T = "rule_template"


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
