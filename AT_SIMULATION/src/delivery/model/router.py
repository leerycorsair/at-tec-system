from fastapi import APIRouter, Depends

from src.delivery.core.models.conversions import (
    InternalServiceError,
    SuccessResponse,
    to_ObjectIDResponse,
)
from src.delivery.core.models.models import CommonResponse, ObjectIDResponse
from src.delivery.model.dependencies import (
    IModelService,
    get_current_user,
    get_model_service,
)
from src.delivery.model.models.conversions import to_ModelMetaDB, to_ModelMetasResponse
from src.delivery.model.models.models import ModelMetaRequest, ModelMetasResponse


router = APIRouter(
    prefix="/models",
    tags=["models"],
)


@router.post("", response_model=CommonResponse[ObjectIDResponse | None])
async def create_model(
    body: ModelMetaRequest,
    user_id: int = Depends(get_current_user),
    model_service: IModelService = Depends(get_model_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                model_service.create_model(to_ModelMetaDB(body, user_id))
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get("", response_model=CommonResponse[ModelMetasResponse | None])
async def get_models(
    user_id: int = Depends(get_current_user),
    model_service: IModelService = Depends(get_model_service),
) -> CommonResponse[ModelMetasResponse]:
    try:
        return SuccessResponse(to_ModelMetasResponse(model_service.get_models(user_id)))
    except Exception as e:
        return InternalServiceError(e)


@router.put("/{model_id}", response_model=CommonResponse[ObjectIDResponse | None])
async def update_model(
    body: ModelMetaRequest,
    user_id: int = Depends(get_current_user),
    model_service: IModelService = Depends(get_model_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                model_service.update_model(to_ModelMetaDB(body, user_id))
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.delete("/{model_id}", response_model=CommonResponse[ObjectIDResponse | None])
async def delete_model(
    model_id: int,
    user_id: int = Depends(get_current_user),
    model_service: IModelService = Depends(get_model_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(model_service.delete_model(model_id, user_id))
        )
    except Exception as e:
        return InternalServiceError(e)


# TODO: нужно придумать как не писать ID'шники, но сохранить связи
# models / import
# models / {model_id} / export
