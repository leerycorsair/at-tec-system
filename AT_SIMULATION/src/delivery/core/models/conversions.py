from http import HTTPStatus
from fastapi.responses import JSONResponse
from src.delivery.core.models.models import T, CommonResponse, ObjectIDResponse


def to_ObjectIDResponse(object_id: int) -> ObjectIDResponse:
    return ObjectIDResponse(id=object_id)


def SuccessResponse(data: T) -> CommonResponse[T]:
    return CommonResponse(
        status_code=HTTPStatus.OK.value,
        is_error=False,
        error_message="Success",
        data=data,
    )


def InternalServiceError(exception: Exception) -> JSONResponse:
    response_content = CommonResponse[None](
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        is_error=True,
        error_message=str(exception),
    )

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content=response_content.model_dump(),
    )


def BadRequestError(exception: BaseException) -> CommonResponse[None]:
    return CommonResponse(
        status_code=HTTPStatus.BAD_REQUEST.value,
        is_error=True,
        error_message=str(exception),
    )
