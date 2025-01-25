import enum

from sqlalchemy import (JSON, Boolean, Column, Enum, ForeignKey, Integer,
                        String, UniqueConstraint)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from src.schema.base import Base


class ResourceTypeTypeEnum(enum.Enum):
    CONSTANT = "CONSTANT"
    TEMPORAL = "TEMPORAL"


class ResourceType(Base):
    __tablename__ = "resource_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum(ResourceTypeTypeEnum), nullable=False)

    attributes = relationship("ResourceTypeAttribute", cascade="all, delete-orphan")
    resources = relationship("Resource", cascade="all, delete-orphan")
    rel_resources = relationship("RelevantResource", cascade="all, delete-orphan")
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
    resource_attributes = relationship("ResourceAttribute", cascade="all, delete-orphan")

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

    attributes = relationship("ResourceAttribute", cascade="all, delete-orphan")
    usage_resources = relationship("TemplateUsageArgument", cascade="all, delete-orphan")
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
    value = Column(JSON, nullable=False)

    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    rta_id = Column(Integer, ForeignKey("resource_type_attributes.id"), nullable=False)
