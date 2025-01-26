from typing import List, Protocol

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


_: IProcessorService = ProcessorService(..., ...)  # type: ignore[arg-type, reportArgumentType]
