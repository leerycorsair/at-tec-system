from typing import List, Optional
import uuid

from src.delivery.websocket_manager import WebsocketManager
from src.service.processor.dependencies import IFileRepository, IModelService
from src.service.processor.models.models import Process, ProcessStatus
import subprocess
import threading
import json


class ProcessorService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(
        self,
        model_service: IModelService,
        file_repository: IFileRepository,
        websocket_manager: WebsocketManager,
    ) -> None:
        self._model_service = model_service
        self._file_repository = file_repository
        self._websocket_manager = websocket_manager
        self._processes: List[Process] = []

    def create_process(
        self, user_id: int, file_uuid: str, process_name: str
    ) -> Process:
        file_path = self._file_repository.fetch_file(file_uuid, "/bin")

        process_handle = subprocess.Popen(
            [file_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        process_id = str(uuid.uuid4())

        new_process = Process(
            user_id=user_id,
            process_id=process_id,
            process_name=process_name,
            file_uuid=file_uuid,
            status=ProcessStatus.PAUSE,
            current_tick=0,
            process_handle=process_handle,
        )

        self._processes.append(new_process)
        return new_process

    async def run_process(
        self,
        user_id: int,
        process_id: int,
        ticks: int,
        delay: int,
    ) -> None:
        process = self._find_process_by_id(process_id)
        if not process:
            raise ValueError("Process not found.")

        if process.status not in [ProcessStatus.PAUSE, ProcessStatus.RUNNING]:
            raise ValueError("Process is not in a valid state to run.")

        process.status = ProcessStatus.RUNNING
        command = "RUN\n"
        process.process_handle.stdin.write(command)
        command = f"{ticks} {delay}\n"
        process.process_handle.stdin.write(command)
        process.process_handle.stdin.flush()

        def stream_output():
            for line in process.process_handle.stdout:
                try:
                    json_data = json.loads(line.strip())
                    websocket.send_json(json_data)
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    websocket.close()
                    raise e

        threading.Thread(target=stream_output, daemon=True).start()

    def pause_process(self, user_id: int, process_id: int) -> Process:
        process = self._find_process_by_id(process_id)
        if not process:
            raise ValueError("Process not found.")

        if process.status != ProcessStatus.RUNNING:
            raise ValueError("Process is not currently running.")

        process.process_handle.stdin.write("PAUSE\n")
        process.process_handle.stdin.flush()
        process.status = ProcessStatus.PAUSE

    def kill_process(self, user_id: int, process_id: int) -> Process:
        process = self._find_process_by_id(process_id)
        if not process:
            raise ValueError("Process not found.")

        process.process_handle.stdin.write("KILL\n")
        process.process_handle.stdin.flush()
        process.process_handle.terminate()
        process.status = ProcessStatus.KILLED

    def get_processes(self, user_id: int) -> List[Process]:
        return [process for process in self._processes if process.user_id == user_id]

    def _find_process_by_id(self, process_id: int) -> Optional[Process]:
        for process in self._processes:
            if process.process_id == process_id:
                return process
        return None
