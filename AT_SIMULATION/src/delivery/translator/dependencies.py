from typing import List, Protocol

from fastapi import Depends

from src.service.translator.dependencies import (
    IFileRepository,
    IModelService,
    get_file_repository,
    get_model_service,
)
from src.service.translator.models.models import FileMeta, TranslateInfo
from src.service.translator.service import TranslatorService


class ITranslatorService(Protocol):
    def translate_model(self, model_id: int, user_id: int, file_name: str) -> TranslateInfo: ...

    def get_translated_files(self, user_id: int) -> List[FileMeta]: ...


def get_translator_service(
    model_service: IModelService = Depends(get_model_service),
    file_repository: IFileRepository = Depends(get_file_repository),
) -> ITranslatorService:
    return TranslatorService(
        model_service,
        file_repository,
    )
