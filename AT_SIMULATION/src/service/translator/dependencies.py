from typing import List, Protocol

from fastapi import Depends

from src.repository.minio.models.models import MinioFile
from src.repository.minio.repository import MinioRepository
from src.service.model.dependencies import (IModelRepository,
                                            get_function_service,
                                            get_model_repository,
                                            get_resource_service,
                                            get_template_service)
from src.service.model.models.models import Model
from src.service.model.service import ModelService
from src.storage.minio.storage import get_minio_storage


class IModelService(Protocol):
    def get_model(self, model_id: int, user_id: int) -> Model: ...
    def check_model_rights(self, model_id: int, user_id: int) -> None: ...


def get_model_service(
    model_rep: IModelRepository = Depends(get_model_repository),
    resource_service=Depends(get_resource_service),
    template_service=Depends(get_template_service),
    function_service=Depends(get_function_service),
) -> IModelService:
    return ModelService(
        model_rep,
        resource_service,
        template_service,
        function_service,
    )


class IFileRepository(Protocol):
    def load_file(
        self, user_id: int, file_path: str, file_name: str, model_id: int
    ) -> str: ...

    def get_files(self, user_id: int) -> List[MinioFile]: ...


def get_file_repository(minio_info=Depends(get_minio_storage)) -> IFileRepository:
    client, bucket_name = minio_info
    return MinioRepository(client, bucket_name)
