from pydantic import BaseModel


class ObjectIDResponse(BaseModel):
    id: int
