from typing import List
from fastapi import APIRouter, Depends

from src.delivery.model.dependencies import get_current_model
from src.service.editor.resource.models.models import (
    CreateResourceTypeRequest,
    GetResourceTypeResponse,
    GetResourceTypesResponse,
    UpdateResourceTypeRequest,
)

router = APIRouter(
    prefix="/resources",
    tags=["editor:resources"],
)


@router.post("/types", response_model=int)
async def create_resource_type(
    body: CreateResourceTypeRequest,
    model_id: int = Depends(get_current_model),
):
    pass


## Chech rights
@router.get("/types", response_model=GetResourceTypesResponse)
async def get_resource_types(model_id: int = Depends(get_current_model)):
    pass


## Chech rights
@router.get("/types/{resource_type_id}", response_model=GetResourceTypeResponse)
async def get_resource_type(
    resource_type_id, model_id: int = Depends(get_current_model)
):
    pass


## Chech rights
@router.put("/types/{resource_type_id}", response_model=int)
async def update_resource_type(
    body: UpdateResourceTypeRequest, model_id: int = Depends(get_current_model)
):
    pass

## Chech rights
@router.delete("/types/{resource_type_id}", response_model=int)
async def delete_resource_type(
    resource_type_id, model_id: int = Depends(get_current_model)
):
    pass


# type_id сразу давать
@router.post("/", response_model=int)
async def create_resource(body: Resource):
    pass


# здесь просто название типа
@router.get("/", response_model=List[Resource])
async def get_resources():
    pass


@router.get("/{resource_id}", response_model=Resource)
async def get_resource():
    pass


@router.put("/{resource_id}", response_model=int)
async def update_resource(body: Resource):
    pass


@router.delete("/{resource_id}", response_model=int)
async def delete_resource():
    pass
