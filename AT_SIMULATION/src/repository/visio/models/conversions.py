from src.repository.visio.models.models import (
    EdgeDB,
    NodeDB,
    NodeTablesEnum,
    NodeTypesEnum,
)
from src.schema.function import Function
from src.schema.resource import Resource, ResourceType
from src.schema.template import Template, TemplateUsage
from src.schema.visio import Edge, Node


def to_Node(node: NodeDB) -> Node:
    return Node(
        object_table=node.object_table.value.__tablename__,
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


_tables = {
    NodeTablesEnum.RESOURCE.value.__tablename__: NodeTablesEnum.RESOURCE,
    NodeTablesEnum.RESOURCE_TYPE.value.__tablename__: NodeTablesEnum.RESOURCE_TYPE,
    NodeTablesEnum.FUNCTION.value.__tablename__: NodeTablesEnum.FUNCTION,
    NodeTablesEnum.TEMPLATE.value.__tablename__: NodeTablesEnum.TEMPLATE,
    NodeTablesEnum.TEMPLATE_USAGE.value.__tablename__: NodeTablesEnum.TEMPLATE_USAGE,
}


def to_NodeTablesEnum_from_name(tablename: str) -> NodeTablesEnum:
    return _tables.get(tablename)


_object_tables = {
    NodeTypesEnum.RESOURCE_TYPE: ResourceType,
    NodeTypesEnum.RESOURCE: Resource,
    NodeTypesEnum.FUNCTION: Function,
    NodeTypesEnum.IRREGULAR_EVENT_U: TemplateUsage,
    NodeTypesEnum.IRREGULAR_EVENT_T: Template,
    NodeTypesEnum.OPERATION_U: TemplateUsage,
    NodeTypesEnum.OPERATION_T: Template,
    NodeTypesEnum.RULE_U: TemplateUsage,
    NodeTypesEnum.RULE_T: Template,
}


def to_NodeTablesEnum_from_node_type(node_type: NodeTypesEnum) -> NodeTablesEnum:
    return NodeTablesEnum(_object_tables.get(node_type))


def to_NodeDB(node: Node) -> NodeDB:
    return NodeDB(
        id=node.id,
        object_table=to_NodeTablesEnum_from_name(node.object_table),
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
        to_node=edge.to_node,
        model_id=edge.model_id,
    )


def to_EdgeDB(edge: Edge) -> EdgeDB:
    return EdgeDB(
        id=edge.id,
        from_node=edge.from_node,
        to_node=edge.to_node,
        model_id=edge.model_id,
    )
