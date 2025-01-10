from enum import Enum
from pydantic import BaseModel
from typing import List


class RelevantResourceDB(BaseModel):
    id: int
    name: str
    template_id: int
    resource_type_id: int

class TemplateTypeEnum(str, Enum):
    IRREGULAR_EVENT = "IRREGULAR_EVENT"
    OPERATION = "OPERATION"
    RULE = "RULE"

class TemplateMetaDB(BaseModel):
    id: int
    name: str
    type: TemplateTypeEnum
    rel_resources: List[RelevantResourceDB]
    model_id: int


class OperationBodyDB(BaseModel):
    condition: str
    body_before: str
    delay: int
    body_after: str
    template_id: int


class OperationDB(BaseModel):
    meta: TemplateMetaDB
    body: OperationBodyDB


class RuleBodyDB(BaseModel):
    condition: str
    body: str
    template_id: int


class RuleDB(BaseModel):
    meta: TemplateMetaDB
    body: RuleBodyDB


class IrregularEventBodyDB(BaseModel):
    body: str
    template_id: int


class IrregularEventGeneratorDB(BaseModel):
    type: str
    value: float
    dispersion: float
    template_id: int


class IrregularEventDB(BaseModel):
    meta: TemplateMetaDB
    generator: IrregularEventGeneratorDB
    body: IrregularEventBodyDB


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
