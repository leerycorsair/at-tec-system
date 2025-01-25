import asyncio
import json
import subprocess
import uuid
from typing import List

from src.core.errors import ForbiddenError, NotFoundError, WrapMethodsMeta
from src.service.processor.dependencies import IFileRepository
from src.service.processor.models.models import Process, ProcessStatus
from src.service.websocket_manager.service import WebsocketManager


class ProcessorService(metaclass=WrapMethodsMeta):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(
        self,
        file_repository: IFileRepository,
        websocket_manager: WebsocketManager,
    ) -> None:
        self._file_repository = file_repository
        self._websocket_manager = websocket_manager
        self._processes: List[Process] = []

    def create_process(
        self, user_id: int, file_uuid: str, process_name: str
    ) -> Process:
        self._check_file_rights(user_id, file_uuid)
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
        process_id: str,
        ticks: int,
        delay: int,
    ) -> Process:
        self._check_process_rights(user_id, process_id)

        process = self._find_process_by_id(process_id)
        if not process:
            raise ValueError("Process not found.")

        if process.status not in [ProcessStatus.PAUSE, ProcessStatus.RUNNING]:
            raise ValueError("Process is not in a valid state to run.")

        process.status = ProcessStatus.RUNNING
        try:
            process.process_handle.stdin.write("RUN\n")
            process.process_handle.stdin.write(f"{ticks} {delay}\n")
            process.process_handle.stdin.flush()
        except Exception as e:
            raise RuntimeError(f"Failed to send commands to the process: {e}")

        async def stream_output():
            try:
                while True:
                    line = await asyncio.get_event_loop().run_in_executor(
                        None, process.process_handle.stdout.readline
                    )
                    if not line:
                        break

                    try:
                        json_data = json.loads(line.strip())
                        await self._websocket_manager.send_message(
                            json.dumps(json_data), user_id, process_id
                        )
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error sending message to WebSocket: {e}")
            except Exception as e:
                print(f"Error reading process output: {e}")
            finally:
                process.process_handle.stdout.close()

        asyncio.create_task(stream_output())

        return Process(
            user_id=user_id,
            process_id=process_id,
            process_name=process.process_name,
            file_uuid=process.file_uuid,
            status=ProcessStatus.RUNNING,
            current_tick=0,
            process_handle=process.process_handle,
        )

    def pause_process(self, user_id: int, process_id: str) -> Process:
        self._check_process_rights(user_id, process_id)

        process = self._find_process_by_id(process_id)
        if process.status != ProcessStatus.RUNNING:
            raise ValueError("Process is not currently running.")

        process.process_handle.stdin.write("PAUSE\n")
        process.process_handle.stdin.flush()
        process.status = ProcessStatus.PAUSE

        return process

    def kill_process(self, user_id: int, process_id: str) -> Process:
        self._check_process_rights(user_id, process_id)

        process = self._find_process_by_id(process_id)
        if process.status == ProcessStatus.KILLED:
            raise ValueError("Process is already killed.")

        process.process_handle.stdin.write("KILL\n")
        process.process_handle.stdin.flush()
        process.process_handle.terminate()
        process.status = ProcessStatus.KILLED

        return process

    def get_processes(self, user_id: int) -> List[Process]:
        return [process for process in self._processes if process.user_id == user_id]

    def _find_process_by_id(self, process_id: str) -> Process:
        for process in self._processes:
            if process.process_id == process_id:
                return process
        raise NotFoundError(f"Process {process_id} not found.")

    def _check_file_rights(self, user_id: int, file_uuid: str):
        file = self._file_repository.get_file(file_uuid)
        if file.file_meta.user_id != user_id:
            raise ForbiddenError(f"File {file_uuid} does not belong to user {user_id}")

    def _check_process_rights(self, user_id: int, process_id: str):
        process = self._find_process_by_id(process_id)
        if process.user_id != user_id:
            raise ForbiddenError(
                f"Process {process_id} does not belong to user {user_id}"
            )
