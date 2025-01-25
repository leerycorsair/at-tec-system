from enum import Enum
from typing import List

from pydantic import BaseModel


class ProcessStatusEnum(str, Enum):
    PAUSE = "PAUSE"
    RUNNING = "RUNNING"
    KILLED = "KILLED"


class ProcessResponse(BaseModel):
    id: str
    name: str
    file_id: str
    status: ProcessStatusEnum
    current_tick: int


class ProcessesResponse(BaseModel):
    processes: List[ProcessResponse]
    total: int


class CreateProcessRequest(BaseModel):
    file_id: str
    process_name: str


class RunProcessRequest(BaseModel):
    ticks: int
    delay: int
