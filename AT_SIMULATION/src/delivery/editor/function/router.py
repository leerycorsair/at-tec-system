from fastapi import APIRouter, Depends
from src.delivery.core.models.conversions import (
    SuccessResponse,
    InternalServiceError,
    to_ObjectIDResponse,
)
from src.delivery.core.models.models import CommonResponse, ObjectIDResponse
from src.delivery.editor.function.dependencies import (
    IFunctionService,
    get_function_service,
)
from src.delivery.editor.function.models.conversions import (
    to_FunctionDB,
    to_FunctionResponse,
    to_FunctionsResponse,
)
from src.delivery.editor.function.models.models import (
    FunctionRequest,
    FunctionResponse,
    FunctionsResponse,
)
from src.delivery.model.dependencies import get_current_model

router = APIRouter(
    prefix="/functions",
    tags=["editor:functions"],
)

@router.post("", response_model=CommonResponse[ObjectIDResponse | None])
async def create_function(
    body: FunctionRequest,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                function_service.create_function(to_FunctionDB(body, model_id))
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get("", response_model=CommonResponse[FunctionsResponse | None])
async def get_functions(
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> CommonResponse[FunctionsResponse]:
    try:
        return SuccessResponse(
            to_FunctionsResponse(function_service.get_functions(model_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get("/{function_id}", response_model=CommonResponse[FunctionResponse | None])
async def get_function(
    function_id: int,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> CommonResponse[FunctionResponse]:
    try:
        return SuccessResponse(
            to_FunctionResponse(function_service.get_function(function_id, model_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.put("/{function_id}", response_model=CommonResponse[ObjectIDResponse | None])
async def update_function(
    body: FunctionRequest,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                function_service.update_function(to_FunctionDB(body, model_id))
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.delete("/{function_id}", response_model=CommonResponse[ObjectIDResponse | None])
async def delete_function(
    function_id: int,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                function_service.delete_function(function_id, model_id)
            )
        )
    except Exception as e:
        return InternalServiceError(e)
