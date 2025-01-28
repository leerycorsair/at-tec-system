from datetime import datetime
from enum import Enum
from typing import List, TypedDict, Union


class TranslatedFileDict(TypedDict):
    id: str
    name: str
    model_id: int
    created_at: datetime
    size: int
    model_name: str


class ProcessStatusEnum(str, Enum):
    PAUSE = "PAUSE"
    RUNNING = "RUNNING"
    KILLED = "KILLED"


class ProcessDict(TypedDict):
    id: str
    name: str
    file_id: str
    status: ProcessStatusEnum
    current_tick: int


class ResourceDict(TypedDict, total=False):
    resource_name: str


class UsageIrregularEventDict(TypedDict):
    has_triggered: bool
    usage_name: str
    usage_type: str


class UsageOperationDict(TypedDict):
    has_triggered_after: bool
    has_triggered_before: bool
    usage_name: str
    usage_type: str


class UsageRuleDict(TypedDict):
    has_triggered: bool
    usage_name: str
    usage_type: str


class TickDict(TypedDict):
    current_tick: int
    current_state: ProcessStatusEnum
    resources: List[ResourceDict]
    usages: List[Union[UsageIrregularEventDict, UsageOperationDict, UsageRuleDict]]
