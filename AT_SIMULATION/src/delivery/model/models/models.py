from datetime import datetime
from typing import List
from pydantic import BaseModel


class ModelMeta(BaseModel):
    id: int
    name: str
    created_at: datetime


class CreateModelRequest(BaseModel):
    name: str


class CreateModelResponse(ModelMeta):
    pass


class UpdateModelRequest(BaseModel):
    name: str


class UpdateModelResponse(ModelMeta):
    pass


class DeleteModelResponse(ModelMeta):
    pass


class GetModelsResponse(BaseModel):
    models: List[ModelMeta]
    total: int


# class GetModelResponse(ModelMeta):
#     resource_types: List[ResourceType]
#     resources: List[Resource]
#     functions: List[Function]

#     irregular_events: List[IrregularEventTemplate]
#     operations: List[OperationTemplate]
#     rules: List[RuleTemplate]
#     template_usages: List[TemplateUsage]

#     nodes: List[Node]
#     edges: List[Edge]
