from fastapi import Depends

from src.providers.minio import get_minio_repository
from src.providers.model import get_model_service
from src.repository.minio.repository import MinioRepository
from src.service.model.service import ModelService
from src.service.translator.service import TranslatorService


def get_translator_service(
    model_service: ModelService = Depends(get_model_service),
    file_repository: MinioRepository = Depends(get_minio_repository),
) -> TranslatorService:
    return TranslatorService(
        model_service,
        file_repository,
    )
