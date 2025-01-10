from fastapi import APIRouter, Depends

from src.delivery.core.models.conversions import (
    InternalServiceError,
    SuccessResponse,
    to_ObjectIDResponse,
)
from src.delivery.core.models.models import CommonResponse, ObjectIDResponse
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


@router.post("/types", response_model=CommonResponse[ObjectIDResponse | None])
async def create_resource_type(
    body: ResourceTypeRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                resource_service.create_resource_type(to_ResourceTypeDB(body, model_id))
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get("/types", response_model=CommonResponse[ResourceTypesResponse | None])
async def get_resource_types(
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ResourceTypesResponse]:
    try:
        return SuccessResponse(
            to_ResourceTypesResponse(resource_service.get_resource_types(model_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get(
    "/types/{resource_type_id}",
    response_model=CommonResponse[ResourceTypeResponse | None],
)
async def get_resource_type(
    resource_type_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ResourceTypeResponse]:
    try:
        return SuccessResponse(
            to_ResourceTypeResponse(
                resource_service.get_resource_type(resource_type_id, model_id)
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.put(
    "/types/{resource_type_id}", response_model=CommonResponse[ObjectIDResponse | None]
)
async def update_resource_type(
    body: ResourceTypeRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                resource_service.update_resource_type(
                    to_ResourceTypeDB(body, model_id),
                )
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.delete(
    "/types/{resource_type_id}", response_model=CommonResponse[ObjectIDResponse | None]
)
async def delete_resource_type(
    resource_type_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                resource_service.delete_resource_type(resource_type_id, model_id)
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.post("", response_model=CommonResponse[ObjectIDResponse | None])
async def create_resource(
    body: ResourceRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                resource_service.create_resource(
                    to_ResourceDB(body, model_id),
                )
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get("", response_model=CommonResponse[ResourcesResponse | None])
async def get_resources(
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ResourcesResponse]:
    try:
        return SuccessResponse(
            to_ResourcesResponse(
                resource_service.get_resources(model_id),
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get("/{resource_id}", response_model=CommonResponse[ResourceResponse | None])
async def get_resource(
    resource_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ResourceResponse]:
    try:
        return SuccessResponse(
            to_ResourceResponse(resource_service.get_resource(resource_id, model_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.put("/{resource_id}", response_model=CommonResponse[ObjectIDResponse | None])
async def update_resource(
    body: ResourceRequest,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(
                resource_service.update_resource(
                    to_ResourceDB(body, model_id),
                )
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.delete("/{resource_id}", response_model=CommonResponse[ObjectIDResponse | None])
async def delete_resource(
    resource_id: int,
    model_id: int = Depends(get_current_model),
    resource_service: IResourceService = Depends(get_resource_service),
) -> CommonResponse[ObjectIDResponse]:
    try:
        return SuccessResponse(
            to_ObjectIDResponse(resource_service.delete_resource(resource_id, model_id))
        )
    except Exception as e:
        return InternalServiceError(e)
