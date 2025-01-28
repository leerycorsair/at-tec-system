from typing import List, Protocol

from src.client.auth_client import AuthClient
from src.repository.minio.models.models import MinioFile
from src.repository.model.models.models import ModelMetaDB
from src.service.model.service import ModelService
from src.service.processor.models.models import Process
from src.service.processor.service import ProcessorService
from src.service.translator.service import TranslatorService


class ITranslatorService(Protocol):
    def get_translated_files(self, user_id: int) -> List[MinioFile]: ...


_: ITranslatorService = TranslatorService(..., ...)  # type: ignore[arg-type, reportArgumentType]


class IModelService(Protocol):
    def get_models(self, user_id: int) -> List[ModelMetaDB]: ...


_: IModelService = ModelService(..., ..., ..., ...)  # type: ignore[arg-type, reportArgumentType]


class IAuthClient(Protocol):
    async def verify_token(self, token: str) -> int: ...


_: IAuthClient = AuthClient(...)  # type: ignore[arg-type, reportArgumentType]


class IProcessorService(Protocol):
    def create_process(
        self, user_id: int, file_uuid: str, process_name: str
    ) -> Process: ...

    async def run_tick(self, user_id: int, process_id: str) -> dict: ...

    def kill_process(self, user_id: int, process_id: str) -> Process: ...

    def get_processes(self, user_id: int) -> List[Process]: ...


_: IProcessorService = ProcessorService(..., ...)  # type: ignore[arg-type, reportArgumentType]
