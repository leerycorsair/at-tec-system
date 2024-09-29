from fastapi import APIRouter, Depends
from src.delivery.core.models.conversions import to_ObjectIDResponse
from src.delivery.core.models.models import ObjectIDResponse
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
from src.service.editor.function.models.models import Function

router = APIRouter(
    prefix="/functions",
    tags=["editor:functions"],
)


@router.post("/", response_model=ObjectIDResponse)
async def create_function(
    body: FunctionRequest,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await function_service.create_function(to_FunctionDB(body, model_id))
    )


@router.get("/", response_model=FunctionsResponse)
async def get_functions(
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> FunctionsResponse:
    return to_FunctionsResponse(await function_service.get_functions(model_id))


@router.get("/{function_id}", response_model=Function)
async def get_function(
    function_id: int,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> FunctionResponse:
    return to_FunctionResponse(
        await function_service.get_function(function_id, model_id)
    )


@router.put("/{function_id}", response_model=ObjectIDResponse)
async def update_function(
    body: FunctionRequest,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await function_service.update_function(to_FunctionDB(body, model_id))
    )


@router.delete("/{function_id}", response_model=ObjectIDResponse)
async def delete_function(
    function_id: int,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await function_service.delete_function(function_id, model_id)
    )
