from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
    UniqueConstraint,
    event,
)

from sqlalchemy.engine import Connection

from src.schema.function import Function
from src.schema.resource import Resource, ResourceType
from src.schema.template import Template, TemplateUsage

from .base import Base

import enum


class NodeType(enum.Enum):
    RESOURCE = "RESOURCE"
    RESOURCE_TYPE = "RESOURCE_TYPE"
    FUNCTION = "FUNCTION"

    RULE_TEMPLATE = "RULE_TEMPLATE"
    RULE_TEMPLATE_USAGE = "RULE_TEMPLATE_USAGE"

    OPERATION_TEMPLATE = "OPERATION_TEMPLATE"
    OPERATION_TEMPLATE_USAGE = "OPERATION_TEMPLATE_USAGE"

    IRREGULAR_TEMPLATE = "IRREGULAR_TEMPLATE"
    IRREGULAR_TEMPLATE_USAGE = "IRREGULAR_TEMPLATE_USAGE"


class TableType(enum.Enum):
    RESOURCES = "resources"
    RESOURCE_TYPES = "resource_types"
    FUNCTIONS = "functions"
    TEMPLATES = "templates"
    TEMPLATE_USAGES = "template_usages"


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_table = Column(String, nullable=False)
    object_name = Column(String, nullable=False)
    object_id = Column(Integer, nullable=False)
    node_type = Column(Enum(NodeType), nullable=False)
    pos_x = Column(Integer, nullable=False)
    pos_y = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    color = Column(String, nullable=False)

    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "object_name",
            "object_table",
            "model_id",
            name="uix_object_name_object_table_model_id",
        ),
    )


def delete_associated_node(connection: Connection, target):
    connection.execute(
        Node.__table__.delete()
        .where(Node.object_table == target.__tablename__)
        .where(Node.object_id == target.id)
    )


event.listen(Resource, "after_delete", delete_associated_node)
event.listen(ResourceType, "after_delete", delete_associated_node)
event.listen(Template, "after_delete", delete_associated_node)
event.listen(TemplateUsage, "after_delete", delete_associated_node)
event.listen(Function, "after_delete", delete_associated_node)


class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, autoincrement=True)

    from_node = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    to_node = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "from_node != to_node",
            name="check_from_node_to_node_diff",
        ),
    )
