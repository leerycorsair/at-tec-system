from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class RelevantResourceRequest(BaseModel):
    id: Optional[int] = None
    name: str
    resource_type_id: int


class RelevantResourceResponse(RelevantResourceRequest):
    id: int


class TemplateTypeEnum(str, Enum):
    IRREGULAR_EVENT = "irregular_event"
    OPERATION = "operation"
    RULE = "rule"


class TemplateMetaRequest(BaseModel):
    id: Optional[int] = None
    name: str
    type: TemplateTypeEnum
    rel_resources: List[RelevantResourceRequest]


class TemplateMetaResponse(TemplateMetaRequest):
    id: int
    rel_resources: List[RelevantResourceResponse]


class OperationBody(BaseModel):
    condition: str
    body_before: str
    delay: int
    body_after: str


class OperationRequest(BaseModel):
    meta: TemplateMetaRequest
    body: OperationBody


class OperationResponse(OperationRequest):
    meta: TemplateMetaResponse


class RuleBody(BaseModel):
    condition: str
    body: str


class RuleRequest(BaseModel):
    meta: TemplateMetaRequest
    body: RuleBody


class RuleResponse(RuleRequest):
    meta: TemplateMetaResponse


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


class IrregularEventResponse(IrregularEventRequest):
    meta: TemplateMetaResponse


class TemplateUsageArgumentRequest(BaseModel):
    id: Optional[int] = None
    relevant_resource_id: int
    resource_id: int


class TemplateUsageRequest(BaseModel):
    id: Optional[int] = None
    name: str
    template_id: int
    arguments: List[TemplateUsageArgumentRequest]


class TemplateUsageArgumentResponse(TemplateUsageArgumentRequest):
    id: int


class TemplateUsageResponse(TemplateUsageRequest):
    id: int
    arguments: List[TemplateUsageArgumentResponse]


class TemplateUsagesResponse(BaseModel):
    usages: List[TemplateUsageResponse]
    total: int


class TemplatesResponse(BaseModel):
    irregular_events: List[IrregularEventResponse]
    operations: List[OperationResponse]
    rules: List[RuleResponse]
    total: int
