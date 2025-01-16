from pydantic import BaseModel


class FileMeta(BaseModel):
    id: int
    name: str
    model_id: int


class TranslateInfo(BaseModel):
    file_id: int
    file_content: str
    translate_logs: str
