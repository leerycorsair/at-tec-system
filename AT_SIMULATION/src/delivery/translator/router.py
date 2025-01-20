from fastapi import APIRouter, Depends
from src.delivery.core.models.conversions import InternalServiceError, SuccessResponse
from src.delivery.core.models.models import CommonResponse
from src.delivery.model.dependencies import get_current_user
from src.delivery.translator.dependencies import (
    ITranslatorService,
    get_translator_service,
)
from src.delivery.translator.models.conversions import (
    to_TranslateResponse,
    to_TranslatedFilesResponse,
)
from src.delivery.translator.models.models import (
    TranslateModelRequest,
    TranslateResponse,
    TranslatedFilesResponse,
)

router = APIRouter(
    prefix="/translator",
    tags=["translator"],
)


@router.get("/files", response_model=CommonResponse[TranslatedFilesResponse | None])
async def get_translated_files(
    user_id: int = Depends(get_current_user),
    translator_service: ITranslatorService = Depends(get_translator_service),
) -> CommonResponse[TranslatedFilesResponse]:
    try:
        return SuccessResponse(
            to_TranslatedFilesResponse(translator_service.get_translated_files(user_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.post(
    "/files/{model_id}", response_model=CommonResponse[TranslateResponse | None]
)
async def translate_model(
    body: TranslateModelRequest,
    model_id: int,
    user_id: int = Depends(get_current_user),
    translator_service: ITranslatorService = Depends(get_translator_service),
) -> CommonResponse[TranslateResponse]:
    try:
        return SuccessResponse(
            to_TranslateResponse(translator_service.translate_model(model_id, user_id, body.file_name))
        )
    except Exception as e:
        return InternalServiceError(e)
