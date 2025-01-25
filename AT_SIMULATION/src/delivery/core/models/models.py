from pydantic import BaseModel


class ObjectIDResponse(BaseModel):
    id: int


def to_ObjectIDResponse(object_id: int) -> ObjectIDResponse:
    return ObjectIDResponse(id=object_id)
