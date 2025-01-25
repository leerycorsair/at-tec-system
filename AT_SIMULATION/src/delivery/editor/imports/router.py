from fastapi import APIRouter, Depends
from src.delivery.core.models.models import (
    to_ObjectIDResponse,
)
from src.delivery.core.models.models import ObjectIDResponse
from src.delivery.editor.imports.dependencies import IImportService, get_import_service
from src.delivery.editor.imports.models.conversions import (
    to_ImportDB,
    to_ImportResponse,
    to_ImportsResponse,
)
from src.delivery.editor.imports.models.models import (
    ImportRequest,
    ImportResponse,
    ImportsResponse,
)
from src.delivery.model.dependencies import get_current_model

router = APIRouter(
    prefix="/imports",
    tags=["editor:imports"],
)


@router.post("", response_model=ObjectIDResponse)
async def create_import(
    body: ImportRequest,
    model_id: int = Depends(get_current_model),
    import_service: IImportService = Depends(get_import_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        import_service.create_import(to_ImportDB(body, model_id))
    )


@router.get("", response_model=ImportsResponse)
async def get_imports(
    model_id: int = Depends(get_current_model),
    import_service: IImportService = Depends(get_import_service),
) -> ImportsResponse:
    return to_ImportsResponse(import_service.get_imports(model_id))


@router.get("/{import_id}", response_model=ImportResponse)
async def get_import(
    import_id: int,
    model_id: int = Depends(get_current_model),
    import_service: IImportService = Depends(get_import_service),
) -> ImportResponse:
    return to_ImportResponse(import_service.get_import(import_id, model_id))


@router.put("/{import_id}", response_model=ObjectIDResponse)
async def update_import(
    body: ImportRequest,
    model_id: int = Depends(get_current_model),
    import_service: IImportService = Depends(get_import_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        import_service.update_import(to_ImportDB(body, model_id))
    )


@router.delete("/{import_id}", response_model=ObjectIDResponse)
async def delete_import(
    import_id: int,
    model_id: int = Depends(get_current_model),
    import_service: IImportService = Depends(get_import_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(import_service.delete_import(import_id, model_id))
