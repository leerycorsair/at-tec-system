from fastapi import Request
from fastapi.exceptions import RequestValidationError

from src.core.errors import BadRequestError


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    raise BadRequestError(str(exc))
