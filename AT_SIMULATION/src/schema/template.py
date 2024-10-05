from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    Enum,
    String,
    Text,
    UniqueConstraint,
)
from src.schema.base import Base

import enum


class TemplateTypeEnum(enum.Enum):
    IRREGULAR_EVENT = "irregular_event"
    OPERATION = "operation"
    RULE = "rule"


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum(TemplateTypeEnum), nullable=False)

    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_template_name_model_id",
        ),
    )


class RelevantResource(Base):
    __tablename__ = "relevant_resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    resource_type_id = Column(Integer, ForeignKey("resource_types.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "template_id",
            name="uix_relevant_resource_name_template_id",
        ),
    )


class TemplateUsage(Base):
    __tablename__ = "template_usages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
        ),
    )


class TemplateUsageArgument(Base):
    __tablename__ = "template_usage_args"

    id = Column(Integer, primary_key=True, autoincrement=True)

    relevant_resource_id = Column(
        Integer, ForeignKey("relevant_resources.id"), nullable=False
    )
    template_usage_id = Column(
        Integer, ForeignKey("template_usages.id"), nullable=False
    )
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)


class IrregularEventBody(Base):
    __tablename__ = "irregular_event_bodies"

    body = Column(Text, nullable=False)

    template_id = Column(Integer, ForeignKey("templates.id"), primary_key=True, nullable=False)


class IrregularEventGeneratorTypeEnum(enum.Enum):
    NORMAL = "normal"
    PRECISE = "precise"
    RANDOM = "random"
    UNIFORM = "uniform"
    EXPONENTIAL = "exponential"
    GAUSSIAN = "gaussian"
    POISSON = "poisson"


class IrregularEventGenerator(Base):
    __tablename__ = "irregular_event_generators"

    type = Column(Enum(IrregularEventGeneratorTypeEnum), nullable=False)
    value = Column(Float, nullable=False)
    dispersion = Column(Float, nullable=False)
    
    template_id = Column(Integer, ForeignKey("templates.id"), primary_key=True, nullable=False)


class OperationBody(Base):
    __tablename__ = "operation_bodies"

    condition = Column(Text, nullable=False)
    body_before = Column(Text, nullable=False)
    delay = Column(Integer, nullable=False)
    body_after = Column(Text, nullable=False)

    template_id = Column(Integer, ForeignKey("templates.id"), primary_key=True, nullable=False)


class RuleBody(Base):
    __tablename__ = "rule_bodies"

    condition = Column(Text, nullable=False)
    body = Column(Text, nullable=False)

    template_id = Column(Integer, ForeignKey("templates.id"), primary_key=True, nullable=False)
