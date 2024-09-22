from fastapi import APIRouter, Depends

from src.delivery.editor.resource.dependencies import (
    IResourceService,
    get_resource_service,
)
from src.delivery.editor.resource.models.conversions import (
    create_to_ResourceDB,
    create_to_ResourceTypeDB,
    to_CreateResourceResponse,
    to_CreateResourceTypeResponse,
    to_DeleteResourceResponse,
    to_DeleteResourceTypeResponse,
    to_GetResourceResponse,
    to_GetResourceTypeResponse,
    to_GetResourceTypesResponse,
    to_GetResourcesResponse,
    to_UpdateResourceResponse,
    to_UpdateResourceTypeResponse,
    update_to_ResourceDB,
    update_to_ResourceTypeDB,
)
from src.delivery.editor.resource.models.models import (
    CreateResourceRequest,
    CreateResourceResponse,
    CreateResourceTypeRequest,
    CreateResourceTypeResponse,
    DeleteResourceResponse,
    DeleteResourceTypeResponse,
    GetResourceResponse,
    GetResourceTypeResponse,
    GetResourceTypesResponse,
    GetResourcesResponse,
    UpdateResourceRequest,
    UpdateResourceResponse,
    UpdateResourceTypeRequest,
    UpdateResourceTypeResponse,
)
from src.delivery.model.dependencies import get_current_model
from src.service.editor.resource.service import ResourceService

router = APIRouter(
    prefix="/resources",
    tags=["editor:resources"],
)


@router.post("/types", response_model=CreateResourceTypeResponse)
async def create_resource_type(
    body: CreateResourceTypeRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CreateResourceTypeResponse:
    return to_CreateResourceTypeResponse(
        await resource_service.create_resource_type(
            create_to_ResourceTypeDB(body, model_id)
        )
    )


@router.get("/types", response_model=GetResourceTypesResponse)
async def get_resource_types(
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> GetResourceTypesResponse:
    return to_GetResourceTypesResponse(
        await resource_service.get_resource_types(model_id)
    )


@router.get("/types/{resource_type_id}", response_model=GetResourceTypeResponse)
async def get_resource_type(
    resource_type_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> GetResourceTypeResponse:
    return to_GetResourceTypeResponse(
        await resource_service.get_resource_type(resource_type_id, model_id)
    )


@router.put("/types/{resource_type_id}", response_model=UpdateResourceTypeResponse)
async def update_resource_type(
    resource_type_id: int,
    body: UpdateResourceTypeRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> UpdateResourceTypeResponse:
    return to_UpdateResourceTypeResponse(
        await resource_service.update_resource_type(
            update_to_ResourceTypeDB(body, model_id, resource_type_id),
        )
    )


@router.delete("/types/{resource_type_id}", response_model=DeleteResourceTypeResponse)
async def delete_resource_type(
    resource_type_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> DeleteResourceTypeResponse:
    return to_DeleteResourceTypeResponse(
        await resource_service.delete_resource_type(resource_type_id, model_id)
    )


@router.post("/", response_model=CreateResourceResponse)
async def create_resource(
    body: CreateResourceRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CreateResourceResponse:
    return to_CreateResourceResponse(
        await resource_service.create_resource(
            create_to_ResourceDB(body, model_id),
        )
    )


@router.get("/", response_model=GetResourcesResponse)
async def get_resources(
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> GetResourcesResponse:
    return to_GetResourcesResponse(
        await resource_service.get_resources(model_id),
    )


@router.get("/{resource_id}", response_model=GetResourceResponse)
async def get_resource(
    resource_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> GetResourceResponse:
    return to_GetResourceResponse(
        await resource_service.get_resource(resource_id, model_id)
    )


@router.put("/{resource_id}", response_model=UpdateResourceResponse)
async def update_resource(
    resource_id: int,
    body: UpdateResourceRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> UpdateResourceResponse:
    return to_UpdateResourceResponse(
        await resource_service.create_resource(
            update_to_ResourceDB(body, model_id, resource_id),
        )
    )


@router.delete("/{resource_id}", response_model=int)
async def delete_resource(
    resource_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(ResourceService),
) -> DeleteResourceResponse:
    return to_DeleteResourceResponse(
        await resource_service.delete_resource(resource_id, model_id)
    )
