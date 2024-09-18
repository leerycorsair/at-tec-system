from enum import Enum
from pydantic import BaseModel
from typing import List


class RelevantResourceDB(BaseModel):
    id: int
    name: str
    template_id: int
    resource_type_id: int


class TemplateTypeEnum(Enum):
    IRREGULAR_EVENT = "irregular_event"
    OPERATION = "operation"
    RULE = "rule"


class TemplateMetaDB(BaseModel):
    id: int
    name: str
    type: TemplateTypeEnum
    rel_resources: List[RelevantResourceDB]
    model_id: int


class OperationBodyDB(BaseModel):
    id: int
    condition: str
    body_before: str
    delay: int
    body_after: str
    template_id: int


class OperationTemplateDB(BaseModel):
    template_meta: TemplateMetaDB
    body: OperationBodyDB


class RuleBodyDB(BaseModel):
    id: int
    condition: str
    body: str
    template_id: int


class RuleTemplateDB(BaseModel):
    template_meta: TemplateMetaDB
    body: RuleBodyDB


class IrregularEventBodyDB(BaseModel):
    id: int
    body: str
    template_id: int


class GeneratorTypeEnum(Enum):
    NORMAL = "normal"
    PRECISE = "precise"
    RANDOM = "random"
    UNIFORM = "uniform"
    EXPONENTIAL = "exponential"
    GAUSSIAN = "gaussian"
    POISSON = "poisson"


class IrregularEventGeneratorDB(BaseModel):
    id: int
    type: GeneratorTypeEnum
    value: float
    dispersion: float
    template_id: int


class IrregularEventTemplateDB(BaseModel):
    template_meta: TemplateMetaDB
    generator: IrregularEventGeneratorDB


class TemplateUsageArgumentDB(BaseModel):
    id: int
    relevant_resource_id: int
    template_usage_id: int
    resource_id: int


class TemplateUsageDB(BaseModel):
    id: int
    name: str
    template_id: int
    arguments: List[TemplateUsageArgumentDB]
    model_id: int
