from typing import List
from src.delivery.translator.models.models import (
    TranslateResponse,
    TranslatedFileResponse,
    TranslatedFilesResponse,
)
from src.service.translator.models.models import FileMeta, TranslateInfo


def to_TranslatedFileResponse(meta: FileMeta) -> TranslatedFileResponse:
    return TranslatedFileResponse(
        id=meta.id,
        name=meta.name,
        model_id=meta.model_id,
    )


def to_TranslatedFilesResponse(metas: List[FileMeta]) -> TranslatedFilesResponse:
    return TranslatedFilesResponse(
        files=[to_TranslatedFileResponse(meta) for meta in metas],
        total=len(metas),
    )


def to_TranslateResponse(info: TranslateInfo) -> TranslateResponse:
    return TranslateResponse(
        file_name=info.file_name,
        file_content=info.file_content,
        translate_logs=info.translate_logs,
        stage=info.stage,
    )

