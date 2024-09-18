from fastapi import APIRouter, Depends

from src.delivery.model.dependencies import (
    check_model_rights,
    get_current_user,
)
from src.dto.api.model.model import (
    CreateModelRequest,
    CreateModelResponse,
    GetModelResponse,
    GetModelsListResponse,
    UpdateModelRequest,
)
from src.service.model.model import ModelService


router = APIRouter(
    prefix="/models",
    tags=["models"],
)


@router.post("/", response_model=CreateModelResponse)
async def create_model(
    body: CreateModelRequest,
    user_id: int = Depends(get_current_user),
    model_service: ModelService = Depends(),
) -> CreateModelResponse:
    return await model_service.create_model(user_id, body)


@router.get("/{model_id}", response_model=GetModelResponse)
async def get_model(
    model_id: int = Depends(check_model_rights),
    model_service: ModelService = Depends(),
) -> GetModelResponse:
    return await model_service.get_model(model_id)


@router.get("/", response_model=GetModelsListResponse)
async def get_models(
    user_id: int = Depends(get_current_user),
    model_service: ModelService = Depends(),
) -> GetModelsListResponse:
    return await model_service.get_models(user_id)


@router.put("/{model_id}", response_model=None)
async def update_model(
    body: UpdateModelRequest,
    model_id: int = Depends(check_model_rights),
    model_service: ModelService = Depends(),
) -> None:
    await model_service.update_model(model_id, body)


@router.delete("/{model_id}", response_model=None)
async def delete_model(
    model_id: int = Depends(check_model_rights),
    model_service: ModelService = Depends(),
) -> None:
    await model_service.delete_model(model_id)


# models / import

# models / {model_id} / export
