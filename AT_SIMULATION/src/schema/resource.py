import enum
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Enum,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY

from src.schema.base import Base


class ResourceTypeTypeEnum(enum.Enum):
    CONSTANT = "CONSTANT"
    TEMPORAL = "TEMPORAL"


class ResourceType(Base):
    __tablename__ = "resource_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum(ResourceTypeTypeEnum), nullable=False)

    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_resource_type_name_model_id",
        ),
    )


class ResourceTypeAttribute(Base):
    __tablename__ = "resource_type_attributes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    default_value = Column(JSON, nullable=True)
    enum_values_set = Column(ARRAY(String), nullable=True)

    resource_type_id = Column(Integer, ForeignKey("resource_types.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "resource_type_id",
            name="uix_resource_type_attribute_name_resource_type_id",
        ),
    )


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    to_be_traced = Column(Boolean, nullable=False)

    resource_type_id = Column(Integer, ForeignKey("resource_types.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_resource_name_model_id",
        ),
    )


class ResourceAttribute(Base):
    __tablename__ = "resource_attributes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=False)

    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    rta_id = Column(Integer, ForeignKey("resource_type_attributes.id"), nullable=False)
