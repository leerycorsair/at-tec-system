import enum

from sqlalchemy import (Column, Enum, Float, ForeignKey, Integer, String, Text,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from src.schema.base import Base


class TemplateTypeEnum(enum.Enum):
    IRREGULAR_EVENT = "IRREGULAR_EVENT"
    OPERATION = "OPERATION"
    RULE = "RULE"


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum(TemplateTypeEnum), nullable=False)

    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    relevant_resources = relationship("RelevantResource", cascade="all, delete")
    template_usages = relationship("TemplateUsage", cascade="all, delete")
    irregular_event_bodies = relationship("IrregularEventBody", cascade="all, delete")
    irregular_event_generators = relationship(
        "IrregularEventGenerator", cascade="all, delete"
    )
    operation_bodies = relationship("OperationBody", cascade="all, delete")
    rule_bodies = relationship("RuleBody", cascade="all, delete")

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
    template_usage_args = relationship("TemplateUsageArgument", cascade="all, delete")

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
    template_usage_args = relationship("TemplateUsageArgument", cascade="all, delete")

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

    template_id = Column(
        Integer, ForeignKey("templates.id"), primary_key=True, nullable=False
    )


class IrregularEventGeneratorTypeEnum(enum.Enum):
    NORMAL = "NORMAL"
    PRECISE = "PRECISE"
    UNIFORM = "UNIFORM"
    EXPONENTIAL = "EXPONENTIAL"
    GAUSSIAN = "GAUSSIAN"
    POISSON = "POISSON"


class IrregularEventGenerator(Base):
    __tablename__ = "irregular_event_generators"

    type = Column(Enum(IrregularEventGeneratorTypeEnum), nullable=False)
    value = Column(Float, nullable=False)
    dispersion = Column(Float, nullable=False)

    template_id = Column(
        Integer, ForeignKey("templates.id"), primary_key=True, nullable=False
    )


class OperationBody(Base):
    __tablename__ = "operation_bodies"

    condition = Column(Text, nullable=False)
    body_before = Column(Text, nullable=False)
    delay = Column(Integer, nullable=False)
    body_after = Column(Text, nullable=False)

    template_id = Column(
        Integer, ForeignKey("templates.id"), primary_key=True, nullable=False
    )


class RuleBody(Base):
    __tablename__ = "rule_bodies"

    condition = Column(Text, nullable=False)
    body = Column(Text, nullable=False)

    template_id = Column(
        Integer, ForeignKey("templates.id"), primary_key=True, nullable=False
    )
