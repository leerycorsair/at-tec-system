

from src.delivery.core.models.models import ObjectIDResponse


def to_ObjectIDResponse(
    object_id: int,
) -> ObjectIDResponse:
    return ObjectIDResponse(id=object_id)