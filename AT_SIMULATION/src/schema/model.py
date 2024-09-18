from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Enum,
    UniqueConstraint,
)
from .base import Base

import enum


class NodeType(enum.Enum):
    RESOURCE = "resource"
    RESOURCE_TYPE = "resource_type"
    FUNCTION = "function"

    RULE_TEMPLATE = "rule_template"
    RULE_TEMPLATE_USAGE = "rule_template_usage"

    OPERATION_TEMPLATE = "operation_template"
    OPERATION_TEMPLATE_USAGE = "operation_template_usage"

    IRREGULAR_TEMPLATE = "irregular_template"
    IRREGULAR_TEMPLATE_USAGE = "irregular_template_usage"


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


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    node_type = Column(Enum(NodeType), nullable=False)
    pos_x = Column(Integer, nullable=False)
    pos_y = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    color = Column(String, nullable=False)

    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_node_name_model_id",
        ),
    )


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    __table_args__ = (
        UniqueConstraint(
            "name",
            "user_id",
            name="uix_model_name_user_id",
        ),
    )
