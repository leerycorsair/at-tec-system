from typing import List, Protocol

from src.repository.minio.models.models import MinioFile
from src.service.translator.models.models import TranslateInfo
from src.service.translator.service import TranslatorService


class ITranslatorService(Protocol):
    def translate_model(
        self, model_id: int, user_id: int, file_name: str
    ) -> TranslateInfo: ...

    def get_translated_files(self, user_id: int) -> List[MinioFile]: ...


_: ITranslatorService = TranslatorService(..., ...)  # type: ignore[arg-type, reportArgumentType]
