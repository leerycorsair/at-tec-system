from datetime import datetime
from typing import List

from pydantic import BaseModel


class TranslatedFileResponse(BaseModel):
    id: str
    name: str
    model_id: int
    created_at: datetime
    size: int


class TranslatedFilesResponse(BaseModel):
    files: List[TranslatedFileResponse]
    total: int


class TranslateResponse(BaseModel):
    id: str
    file_content: str
    translate_logs: str
    stage: str


class TranslateModelRequest(BaseModel):
    name: str
