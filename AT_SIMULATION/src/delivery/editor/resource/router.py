from fastapi import APIRouter, Depends

from src.delivery.core.models.conversions import to_ObjectIDResponse
from src.delivery.core.models.models import ObjectIDResponse
from src.delivery.editor.resource.dependencies import (
    IResourceService,
    get_resource_service,
)
from src.delivery.editor.resource.models.conversions import (
    to_ResourceDB,
    to_ResourceResponse,
    to_ResourceTypeDB,
    to_ResourceTypeResponse,
    to_ResourceTypesResponse,
    to_ResourcesResponse,
)
from src.delivery.editor.resource.models.models import (
    ResourceRequest,
    ResourceResponse,
    ResourceTypeRequest,
    ResourceTypeResponse,
    ResourceTypesResponse,
    ResourcesResponse,
)
from src.delivery.model.dependencies import get_current_model

router = APIRouter(
    prefix="/resources",
    tags=["editor:resources"],
)


@router.post("/types", response_model=ObjectIDResponse)
async def create_resource_type(
    body: ResourceTypeRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        resource_service.create_resource_type(to_ResourceTypeDB(body, model_id))
    )


@router.get("/types", response_model=ResourceTypesResponse)
async def get_resource_types(
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ResourceTypesResponse:
    return to_ResourceTypesResponse(resource_service.get_resource_types(model_id))


@router.get("/types/{resource_type_id}", response_model=ResourceTypeResponse)
async def get_resource_type(
    resource_type_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ResourceTypeResponse:
    return to_ResourceTypeResponse(
        resource_service.get_resource_type(resource_type_id, model_id)
    )


@router.put("/types/{resource_type_id}", response_model=ObjectIDResponse)
async def update_resource_type(
    body: ResourceTypeRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        resource_service.update_resource_type(
            to_ResourceTypeDB(body, model_id),
        )
    )


@router.delete("/types/{resource_type_id}", response_model=ObjectIDResponse)
async def delete_resource_type(
    resource_type_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        resource_service.delete_resource_type(resource_type_id, model_id)
    )


@router.post("/", response_model=ObjectIDResponse)
async def create_resource(
    body: ResourceRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        resource_service.create_resource(
            to_ResourceDB(body, model_id),
        )
    )


@router.get("/", response_model=ResourcesResponse)
async def get_resources(
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ResourcesResponse:
    return to_ResourcesResponse(
        resource_service.get_resources(model_id),
    )


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ResourceResponse:
    return to_ResourceResponse(resource_service.get_resource(resource_id, model_id))


@router.put("/{resource_id}", response_model=ObjectIDResponse)
async def update_resource(
    body: ResourceRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        resource_service.update_resource(
            to_ResourceDB(body, model_id),
        )
    )


@router.delete("/{resource_id}", response_model=ObjectIDResponse)
async def delete_resource(
    resource_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(resource_service.delete_resource(resource_id, model_id))
