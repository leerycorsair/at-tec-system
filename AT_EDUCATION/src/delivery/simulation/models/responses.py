from pydantic import BaseModel


class ObjectIDResponse(BaseModel):
    id: int


class TranslationResponse(BaseModel):
    log: str


class EditorResponse(BaseModel):
    status_code: int
    is_error: bool
    error_message: str
    data: ObjectIDResponse


class TranslatorResponse(BaseModel):
    status_code: int
    is_error: bool
    error_message: str
    data: TranslationResponse
