from pydantic import BaseModel
from typing import List
from enum import Enum


class ProcessStatusEnum(str, Enum):
    PAUSE = "PAUSE"
    RUNNING = "RUNNING"
    KILLED = "KILLED"


class ProcessResponse(BaseModel):
    id: int
    process_name: str
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
