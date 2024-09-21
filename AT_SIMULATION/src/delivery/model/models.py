from datetime import datetime
from pydantic import BaseModel

# class CreateModelRequest(BaseModel):
#     name: str


# class GetModelResponse(BaseModel):
#     id: int
#     name: str
#     created_at: datetime

#     # resource_types: List[ResourceType]
#     # resources: List[Resource]
#     # functions: List[Function]

#     # irregular_events: List[IrregularEventTemplate]
#     # operations: List[OperationTemplate]
#     # rules: List[RuleTemplate]
#     # template_usages: List[TemplateUsage]

#     nodes: List[Node]
#     edges: List[Edge]


# class CreateModelResponse(ModelMeta):
#     pass


# class UpdateModelRequest(BaseModel):
#     name: str


# class UpdateModelResponse(ModelMeta):
#     pass


# class GetModelsListResponse(BaseModel):
#     models: List[ModelMeta]
#     total: int


class CreateModelRequest(BaseModel):
    name: str
    
class CreateModelResponse(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime
    
class GetModelResponse(BaseModel):
    # id: int
    # name: str
    # user_id: int
    # created_at: datetime
    
    # все составляющие с цветами
    pass 


class UpdateModelRequest(BaseModel):
    name: str
