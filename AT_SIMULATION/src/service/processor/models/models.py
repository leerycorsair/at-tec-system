from enum import Enum
import subprocess

from pydantic import BaseModel


class ProcessStatus(str, Enum):
    PAUSE = "PAUSE"
    RUNNING = "RUNNING"
    KILLED = "KILLED"


class Process(BaseModel):
    user_id: int
    process_id: int
    process_name: str
    file_uuid: str
    status: ProcessStatus
    current_tick: int
    process_handle: subprocess.Popen
