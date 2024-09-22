from fastapi import APIRouter, Depends

from src.delivery.model.dependencies import (
    IModelService,
    check_model_rights,
    get_current_user,
    get_model_service,
)

from src.delivery.model.models.conversions import (
    to_CreateModelParamsDB,
    to_CreateModelResponse,
    to_DeleteModelResponse,
    to_GetModelsResponse,
    to_UpdateModelParamsDB,
    to_UpdateModelsResponse,
)
from src.delivery.model.models.models import (
    CreateModelRequest,
    CreateModelResponse,
    DeleteModelResponse,
    GetModelsResponse,
    UpdateModelRequest,
    UpdateModelResponse,
)

router = APIRouter(
    prefix="/models",
    tags=["models"],
)


@router.post("/", response_model=CreateModelResponse)
async def create_model(
    body: CreateModelRequest,
    user_id: int = Depends(get_current_user),
    model_service: IModelService = Depends(get_model_service),
) -> CreateModelResponse:
    params = to_CreateModelParamsDB(body)
    return to_CreateModelResponse(await model_service.create_model(user_id, params))


@router.get("/", response_model=GetModelsResponse)
async def get_models(
    user_id: int = Depends(get_current_user),
    model_service: IModelService = Depends(get_model_service),
) -> GetModelsResponse:
    return to_GetModelsResponse(await model_service.get_models(user_id))


# @router.get("/{model_id}", response_model=GetModelResponse)
# async def get_model(
#     model_id: int = Depends(check_model_rights),
#     model_service: IModelService = Depends(get_model_service),
# ) -> GetModelResponse:
#     return await model_service.get_model(model_id)


@router.put("/{model_id}", response_model=UpdateModelResponse)
async def update_model(
    body: UpdateModelRequest,
    model_id: int = Depends(check_model_rights),
    model_service: IModelService = Depends(get_model_service),
) -> UpdateModelResponse:
    params = to_UpdateModelParamsDB(body)
    return to_UpdateModelsResponse(await model_service.update_model(model_id, params))


@router.delete("/{model_id}", response_model=DeleteModelResponse)
async def delete_model(
    model_id: int = Depends(check_model_rights),
    model_service: IModelService = Depends(get_model_service),
) -> DeleteModelResponse:
    return to_DeleteModelResponse(await model_service.delete_model(model_id))


# models / import

# models / {model_id} / export
