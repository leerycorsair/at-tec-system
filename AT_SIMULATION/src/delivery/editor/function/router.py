from typing import List
from fastapi import APIRouter, Depends
from src.delivery.editor.function.dependencies import (
    IFunctionService,
    get_function_service,
)
from src.delivery.editor.function.models.conversions import (
    create_to_FunctionDB,
    to_CreateFunctionResponse,
    to_DeleteFunctionResponse,
    to_GetFunctionResponse,
    to_GetFunctionsResponse,
    to_UpdateFunctionResponse,
    update_to_FunctionDB,
)
from src.delivery.editor.function.models.models import (
    CreateFunctionRequest,
    CreateFunctionResponse,
    DeleteFunctionResponse,
    GetFunctionResponse,
    GetFunctionsResponse,
    UpdateFunctionRequest,
    UpdateFunctionResponse,
)
from src.delivery.model.dependencies import get_current_model
from src.service.editor.function.models.models import Function

router = APIRouter(
    prefix="/functions",
    tags=["editor:functions"],
)


@router.post("/", response_model=CreateFunctionResponse)
async def create_function(
    body: CreateFunctionRequest,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> CreateFunctionResponse:
    return to_CreateFunctionResponse(
        await function_service.create_function(create_to_FunctionDB(body, model_id))
    )


@router.get("/", response_model=List[Function])
async def get_functions(
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> GetFunctionsResponse:
    return to_GetFunctionsResponse(await function_service.get_functions(model_id))


@router.get("/{function_id}", response_model=Function)
async def get_function(
    function_id: int,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> GetFunctionResponse:
    return to_GetFunctionResponse(
        await function_service.get_function(function_id, model_id)
    )


@router.put("/{function_id}", response_model=int)
async def update_function(
    function_id: int,
    body: UpdateFunctionRequest,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> UpdateFunctionResponse:
    return to_UpdateFunctionResponse(
        await function_service.update_function(
            update_to_FunctionDB(body, model_id, function_id)
        )
    )


@router.delete("/{function_id}", response_model=int)
async def delete_function(
    function_id: int,
    model_id: int = Depends(get_current_model),
    function_service: IFunctionService = Depends(get_function_service),
) -> DeleteFunctionResponse:
    return to_DeleteFunctionResponse(
        await function_service.delete_function(function_id, model_id)
    )
