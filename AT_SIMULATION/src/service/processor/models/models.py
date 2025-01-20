from enum import Enum
import subprocess
from typing import Optional

from pydantic import BaseModel, Field


class ProcessStatus(str, Enum):
    PAUSE = "PAUSE"
    RUNNING = "RUNNING"
    KILLED = "KILLED"


class Process(BaseModel):
    user_id: int
    process_id: str
    process_name: str
    file_uuid: str
    status: ProcessStatus
    current_tick: int
    process_handle: Optional[subprocess.Popen] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
