from typing import Protocol

from src.repository.minio.models.models import MinioFile
from src.repository.minio.repository import MinioRepository
from src.service.model.models.models import Model
from src.service.model.service import ModelService


class IModelService(Protocol):
    def get_model(self, model_id: int, user_id: int) -> Model: ...

    def check_model_rights(self, model_id: int, user_id: int) -> None: ...


_: IModelService = ModelService(..., ..., ..., ...)  # type: ignore[arg-type, reportArgumentType]


class IFileRepository(Protocol):
    def fetch_file(self, file_uuid: str, file_path: str) -> str: ...

    def get_file(self, file_uuid: str) -> MinioFile: ...


_: IFileRepository = MinioRepository(..., ...)  # type: ignore[arg-type, reportArgumentType]
