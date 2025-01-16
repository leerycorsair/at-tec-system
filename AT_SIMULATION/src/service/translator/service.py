from typing import List

from src.service.translator.dependencies import IModelService
from src.service.translator.models.models import FileMeta, TranslateInfo


class TranslatorService:
    def __init__(
        self,
        model_service: IModelService,
    ) -> None:
        self._model_service = model_service

    def translate_model(self, model_id: int, user_id: int) -> TranslateInfo: ...

    def get_translated_files(self, user_id: int) -> List[FileMeta]: ...
