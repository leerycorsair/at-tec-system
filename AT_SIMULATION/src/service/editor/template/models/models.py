from enum import Enum
from pydantic import BaseModel
from typing import List


class RelevantResource(BaseModel):
    name: str
    resource_type_name: str


class TemplateTypeEnum(Enum):
    IRREGULAR_EVENT = "irregular_event"
    OPERATION = "operation"
    RULE = "rule"


class TemplateMeta(BaseModel):
    name: str
    type: TemplateTypeEnum
    rel_resources: List[RelevantResource]


class OperationBody(BaseModel):
    condition: str
    body_before: str
    delay: int
    body_after: str


class OperationTemplate(BaseModel):
    meta: TemplateMeta
    body: OperationBody


class RuleBody(BaseModel):
    condition: str
    body: str


class RuleTemplate(BaseModel):
    meta: TemplateMeta
    body: RuleBody


class IrregularEventBody(BaseModel):
    body: str


class GeneratorTypeEnum(Enum):
    NORMAL = "normal"
    PRECISE = "precise"
    UNIFORM = "uniform"
    EXPONENTIAL = "exponential"
    GAUSSIAN = "gaussian"
    POISSON = "poisson"


class IrregularEventGenerator(BaseModel):
    type: GeneratorTypeEnum
    value: float
    dispersion: float


class IrregularEventTemplate(BaseModel):
    meta: TemplateMeta
    generator: IrregularEventGenerator
    body: IrregularEventBody


class TemplateUsageArgument(BaseModel):
    relevant_resource_name: str
    resource_name: str


class TemplateUsage(BaseModel):
    name: str
    template_name: str
    arguments: List[TemplateUsageArgument]
