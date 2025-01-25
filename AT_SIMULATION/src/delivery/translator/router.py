from fastapi import APIRouter, Depends

from src.delivery.model.dependencies import get_current_user
from src.delivery.translator.dependencies import (ITranslatorService,
                                                  get_translator_service)
from src.delivery.translator.models.conversions import (
    to_TranslatedFilesResponse, to_TranslateResponse)
from src.delivery.translator.models.models import (TranslatedFilesResponse,
                                                   TranslateModelRequest,
                                                   TranslateResponse)

router = APIRouter(
    prefix="/translator",
    tags=["translator"],
)


@router.get("/files", response_model=TranslatedFilesResponse)
async def get_translated_files(
    user_id: int = Depends(get_current_user),
    translator_service: ITranslatorService = Depends(get_translator_service),
) -> TranslatedFilesResponse:
    return to_TranslatedFilesResponse(translator_service.get_translated_files(user_id))


@router.post("/files/{model_id}", response_model=TranslateResponse)
async def translate_model(
    body: TranslateModelRequest,
    model_id: int,
    user_id: int = Depends(get_current_user),
    translator_service: ITranslatorService = Depends(get_translator_service),
) -> TranslateResponse:
    return to_TranslateResponse(
        translator_service.translate_model(model_id, user_id, body.name)
    )
