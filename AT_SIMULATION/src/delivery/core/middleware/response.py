import json
from typing import AsyncIterator, Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.errors import Error, InternalServerError


class ResponseHelper:
    SUCCESS_MESSAGE = "Success"

    IS_ERROR = "is_error"
    STATUS_CODE = "status_code"
    ERROR_MESSAGE = "error_message"
    DATA = "data"

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


class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        try:
            response = await call_next(request)

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

        except Error as e:
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
            return JSONResponse(
                status_code=internal_error.status_code,
                content={
                    ResponseHelper.STATUS_CODE: internal_error.status_code,
                    ResponseHelper.IS_ERROR: True,
                    ResponseHelper.ERROR_MESSAGE: internal_error.http_error,
                },
            )
