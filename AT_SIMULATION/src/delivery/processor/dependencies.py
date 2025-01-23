from typing import List, Protocol

from fastapi import Depends

from src.delivery.websocket_manager import get_websocket_manager
from src.service.processor.dependencies import get_file_repository
from src.service.processor.models.models import Process
from src.service.processor.service import ProcessorService


class IProcessorService(Protocol):
    def create_process(
        self, user_id: int, file_uuid: str, process_name: str
    ) -> Process: ...

    async def run_process(
        self, user_id: int, process_id: str, ticks: int, delay: int
    ) -> Process: ...

    def pause_process(self, user_id: int, process_id: str) -> Process: ...

    def kill_process(self, user_id: int, process_id: str) -> Process: ...

    def get_processes(self, user_id: int) -> List[Process]: ...


def get_processor_service(
    file_repository=Depends(get_file_repository),
    websocket_manager=Depends(get_websocket_manager),
) -> IProcessorService:
    return ProcessorService(
        file_repository,
        websocket_manager,
    )
