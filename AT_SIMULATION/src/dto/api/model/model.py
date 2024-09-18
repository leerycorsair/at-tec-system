from datetime import datetime
from typing import List
from pydantic import BaseModel

from src.dto.api.visio.board import Edge, Node


class CreateModelRequest(BaseModel):
    name: str


class CreateModelResponse(BaseModel):
    id: int
    name: str
    created_at: datetime


class GetModelResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    resource_types: List[ResourceType]
    resources: List[Resource]
    functions: List[Function]

    irregular_events: List[IrregularEventTemplate]
    operations: List[OperationTemplate]
    rules: List[RuleTemplate]
    template_usages: List[TemplateUsage]

    nodes: List[Node]
    edges: List[Edge]


class ModelMeta(BaseModel):
    id: int
    name: str
    created_at: datetime


class GetModelsListResponse(BaseModel):
    models: List[ModelMeta]
    total: int


class UpdateModelRequest(BaseModel):
    name: str
