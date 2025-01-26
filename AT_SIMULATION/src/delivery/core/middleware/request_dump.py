import json
import traceback
from typing import AsyncIterator, Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.config.logger import application_logger as logger
from src.core.errors import Error, InternalServerError


class ResponseHelper:
    SUCCESS_MESSAGE = "Success"

    IS_ERROR = "is_error"
    STATUS_CODE = "status_code"
    ERROR_MESSAGE = "error_message"
    DATA = "data"

    AUTHORIZATION = "authorization"
    REDACTED = "REDACTED"

    @staticmethod
    async def wrap_stream_with_metadata(
        original_stream: AsyncIterator[bytes], metadata: dict
    ) -> AsyncIterator[bytes]:
        yield b"{\n"
        yield f'"{ResponseHelper.STATUS_CODE}": {metadata[ResponseHelper.STATUS_CODE]},\n'.encode()
        yield f'"{ResponseHelper.IS_ERROR}": {json.dumps(metadata[ResponseHelper.IS_ERROR])},\n'.encode()
        yield f'"{ResponseHelper.ERROR_MESSAGE}": {json.dumps(metadata[ResponseHelper.ERROR_MESSAGE])},\n'.encode()
        yield f'"{ResponseHelper.DATA}":\n'.encode()

        first_chunk = True
        async for chunk in original_stream:
            if not first_chunk:
                yield b",\n"
            yield chunk
            first_chunk = False

        yield b"\n}"

    @staticmethod
    def log_request(details: dict, level: str = "info"):
        if level == "info":
            logger.info("Request Log", extra={"details": details})
        elif level == "error":
            logger.error("Request Dump", extra={"details": details})

    @staticmethod
    async def handle_response(request: Request, response: Response) -> Response:
        if isinstance(response, StreamingResponse):
            metadata = {
                ResponseHelper.STATUS_CODE: response.status_code,
                ResponseHelper.IS_ERROR: False,
                ResponseHelper.ERROR_MESSAGE: ResponseHelper.SUCCESS_MESSAGE,
            }
            wrapped_stream = ResponseHelper.wrap_stream_with_metadata(
                response.body_iterator, metadata
            )
            return StreamingResponse(
                wrapped_stream,
                status_code=response.status_code,
                media_type="application/json",
                headers={
                    k: v
                    for k, v in response.headers.items()
                    if k.lower() != "content-length"
                },
            )

        # Parse response body
        response_body = None
        if isinstance(response, JSONResponse):
            response_body = json.loads(response.body.decode())
        elif hasattr(response, "body"):
            response_body = response.body.decode()

        return JSONResponse(
            status_code=response.status_code,
            content={
                ResponseHelper.STATUS_CODE: response.status_code,
                ResponseHelper.IS_ERROR: False,
                ResponseHelper.ERROR_MESSAGE: ResponseHelper.SUCCESS_MESSAGE,
                ResponseHelper.DATA: response_body,
            },
        )


class RequestDumpMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        try:
            response = await call_next(request)

            ResponseHelper.log_request(
                {
                    "method": request.method,
                    "url": str(request.url),
                    ResponseHelper.STATUS_CODE: response.status_code,
                },
                level="info",
            )
            return await ResponseHelper.handle_response(request, response)

        except Error as e:
            log_details = {
                ResponseHelper.STATUS_CODE: e.status_code,
                ResponseHelper.ERROR_MESSAGE: str(e),
                "method": request.method,
                "url": str(request.url),
                "headers": {
                    key: (
                        value
                        if key.lower() != ResponseHelper.AUTHORIZATION
                        else ResponseHelper.REDACTED
                    )
                    for key, value in request.headers.items()
                },
            }
            ResponseHelper.log_request(log_details, level="error")
            return JSONResponse(
                status_code=e.status_code,
                content={
                    ResponseHelper.STATUS_CODE: e.status_code,
                    ResponseHelper.IS_ERROR: True,
                    ResponseHelper.ERROR_MESSAGE: e.http_error,
                },
            )
        except Exception as e:
            internal_error = InternalServerError(str(e))
            log_details = {
                ResponseHelper.STATUS_CODE: internal_error.status_code,
                ResponseHelper.ERROR_MESSAGE: str(internal_error),
                "method": request.method,
                "url": str(request.url),
                "headers": {
                    key: (
                        value
                        if key.lower() != ResponseHelper.AUTHORIZATION
                        else ResponseHelper.REDACTED
                    )
                    for key, value in request.headers.items()
                },
                "trace": traceback.format_exc(),
            }
            ResponseHelper.log_request(log_details, level="error")
            return JSONResponse(
                status_code=internal_error.status_code,
                content={
                    ResponseHelper.STATUS_CODE: internal_error.status_code,
                    ResponseHelper.IS_ERROR: True,
                    ResponseHelper.ERROR_MESSAGE: internal_error.http_error,
                },
            )
