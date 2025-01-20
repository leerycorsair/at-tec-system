from enum import Enum
from pydantic import BaseModel


class StagesEnum(str, Enum):
    FORMATTING = "FORMATTING"
    BUILDING = "BUILDING"
    LINTING = "LINTING"
    COMPLETED = "COMPLETED"


class TranslateInfo(BaseModel):
    file_name: str
    file_content: str
    translate_logs: str
    stage: StagesEnum
