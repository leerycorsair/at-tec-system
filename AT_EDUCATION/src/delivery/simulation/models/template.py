from enum import Enum
from pydantic import BaseModel
from typing import List


class RelevantResourceRequest(BaseModel):
    name: str
    resource_type_id: int


class TemplateTypeEnum(str, Enum):
    IRREGULAR_EVENT = "irregular_event"
    OPERATION = "operation"
    RULE = "rule"


class TemplateMetaRequest(BaseModel):
    name: str
    type: TemplateTypeEnum
    rel_resources: List[RelevantResourceRequest]


class OperationBody(BaseModel):
    condition: str
    body_before: str
    delay: int
    body_after: str


class OperationRequest(BaseModel):
    meta: TemplateMetaRequest
    body: OperationBody


class RuleBody(BaseModel):
    condition: str
    body: str


class RuleRequest(BaseModel):
    meta: TemplateMetaRequest
    body: RuleBody


class IrregularEventBody(BaseModel):
    body: str


class GeneratorTypeEnum(str, Enum):
    NORMAL = "NORMAL"
    PRECISE = "PRECISE"
    UNIFORM = "UNIFORM"
    EXPONENTIAL = "EXPONENTIAL"
    GAUSSIAN = "GAUSSIAN"
    POISSON = "POISSON"


class IrregularEventGenerator(BaseModel):
    type: GeneratorTypeEnum
    value: float
    dispersion: float


class IrregularEventRequest(BaseModel):
    meta: TemplateMetaRequest
    generator: IrregularEventGenerator
    body: IrregularEventBody


class TemplateUsageArgumentRequest(BaseModel):
    relevant_resource_id: int
    resource_id: int


class TemplateUsageRequest(BaseModel):
    name: str
    template_id: int
    arguments: List[TemplateUsageArgumentRequest]
