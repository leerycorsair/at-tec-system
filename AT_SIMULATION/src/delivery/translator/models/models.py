from typing import List
from pydantic import BaseModel


class TranslatedFileResponse(BaseModel):
    id: int
    name: str
    model_id: int


class TranslatedFilesResponse(BaseModel):
    files: List[TranslatedFileResponse]
    total: int


class TranslateResponse(BaseModel):
    file_id: int
    file_content: str
    translate_logs: str
