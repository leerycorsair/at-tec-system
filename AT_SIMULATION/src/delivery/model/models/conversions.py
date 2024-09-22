from typing import List

from src.delivery.model.models.models import (
    CreateModelRequest,
    CreateModelResponse,
    DeleteModelResponse,
    GetModelsResponse,
    ModelMeta,
    UpdateModelRequest,
    UpdateModelResponse,
)
from src.repository.model.models.models import (
    CreateModelParamsDB,
    ModelMetaDB,
    UpdateModelParamsDB,
)


def to_ModelMeta(model: ModelMetaDB) -> ModelMeta:
    return ModelMeta(
        id=model.id,
        name=model.name,
        created_at=model.created_at,
    )


def to_CreateModelResponse(model: ModelMetaDB) -> CreateModelResponse:
    return CreateModelResponse(
        id=model.id,
        name=model.name,
        created_at=model.created_at,
    )


def to_CreateModelParamsDB(request: CreateModelRequest) -> CreateModelParamsDB:
    return CreateModelParamsDB(
        name=request.name,
    )


def to_GetModelsResponse(models: List[ModelMetaDB]) -> GetModelsResponse:
    return GetModelsResponse(
        models=[to_ModelMeta(model) for model in models], total=len(models)
    )


def to_UpdateModelsResponse(model: ModelMetaDB) -> UpdateModelResponse:
    return UpdateModelResponse(
        id=model.id,
        name=model.name,
        created_at=model.created_at,
    )


def to_UpdateModelParamsDB(request: UpdateModelRequest) -> UpdateModelParamsDB:
    return UpdateModelParamsDB(name=request.name)


def to_DeleteModelResponse(model: ModelMetaDB) -> DeleteModelResponse:
    return DeleteModelResponse(
        id=model.id,
        name=model.name,
        created_at=model.created_at,
    )
