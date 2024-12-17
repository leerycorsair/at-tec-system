from pydantic import BaseModel


class SomeResponse(BaseModel):
    status_code: int
    is_error: bool
    error_message: str
    user_message: str
