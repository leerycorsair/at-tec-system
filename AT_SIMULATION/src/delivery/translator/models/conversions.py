from typing import List

from src.delivery.translator.models.models import (
    TranslatedFileResponse,
    TranslatedFilesResponse,
    TranslateResponse,
)
from src.repository.minio.models.models import MinioFile
from src.service.translator.models.models import TranslateInfo


def to_TranslatedFileResponse(file: MinioFile) -> TranslatedFileResponse:
    return TranslatedFileResponse(
        id=file.minio_name,
        name=file.file_meta.file_name,
        model_id=file.file_meta.model_id,
        created_at=file.file_meta.created_at,
        size=file.size,
    )


def to_TranslatedFilesResponse(files: List[MinioFile]) -> TranslatedFilesResponse:
    sorted_files = sorted(
        files, key=lambda file: file.file_meta.created_at, reverse=True
    )
    return TranslatedFilesResponse(
        files=[to_TranslatedFileResponse(file) for file in sorted_files],
        total=len(sorted_files),
    )


def to_TranslateResponse(info: TranslateInfo) -> TranslateResponse:
    return TranslateResponse(
        id=info.file_name,
        file_content=info.file_content,
        translate_logs=info.translate_logs,
        stage=info.stage,
    )
