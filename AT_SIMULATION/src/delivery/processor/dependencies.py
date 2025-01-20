from typing import Protocol

from fastapi import WebSocket


class IProcessorService(Protocol):
    def create_process(self, user_id: int, file_uuid: str, process_name: str): ...

    async def run_process(
        self,
        user_id: int,
        process_id: int,
        ticks: int,
        delay: int,
        web_socket: WebSocket,
    ): ...

    def pause_process(self, user_id: int, process_id: int): ...

    def kill_process(self, user_id: int, process_id: int): ...

    def get_processes(self, user_id: int): ...


def get_processor_service():
    return IProcessorService
