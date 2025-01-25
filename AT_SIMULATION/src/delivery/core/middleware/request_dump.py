import logging
import traceback
from typing import AsyncIterator, Awaitable, Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pythonjsonlogger import jsonlogger
from src.delivery.core.models.errors import Error, InternalServerError
import json

logger = logging.getLogger("request_logger")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def format(self, record):
        log_record = super().format(record)
        try:
            return json.dumps(json.loads(log_record), indent=4)
        except Exception:
            return log_record


formatter = CustomJsonFormatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s %(details)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


from fastapi.responses import StreamingResponse
from starlette.responses import JSONResponse
from typing import AsyncIterator
import json


async def wrap_stream_with_metadata(
    original_stream: AsyncIterator[bytes], metadata: dict
) -> AsyncIterator[bytes]:
    yield b"{\n"
    yield f'"status_code": {metadata["status_code"]},\n'.encode()
    yield f'"is_error": {json.dumps(metadata["is_error"])},\n'.encode()
    yield f'"error_message": {json.dumps(metadata["error_message"])},\n'.encode()
    yield b'"data": [\n'

    first_chunk = True
    async for chunk in original_stream:
        if not first_chunk:
            yield b",\n"
        yield chunk
        first_chunk = False

    yield b"\n]\n}"


async def request_dump(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
):
    try:
        response = await call_next(request)

        if isinstance(response, StreamingResponse):
            metadata = {
                "status_code": response.status_code,
                "is_error": False,
                "error_message": "Success",
            }

            logger.info(
                "Success",
                extra={
                    "details": {
                        "method": request.method,
                        "url": str(request.url),
                        "status_code": response.status_code,
                    }
                },
            )

            wrapped_stream = wrap_stream_with_metadata(response.body_iterator, metadata)

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

        logger.info(
            "Success",
            extra={
                "details": {
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                }
            },
        )

        return JSONResponse(
            status_code=response.status_code,
            content={
                "status_code": response.status_code,
                "is_error": False,
                "error_message": "Success",
                "data": response_body,
            },
        )

    except Error as e:
        log_details = {
            "status_code": e.status_code,
            "error_message": str(e),
            "method": request.method,
            "url": str(request.url),
            "headers": {
                key: value if key.lower() != "authorization" else "REDACTED"
                for key, value in request.headers.items()
            },
        }
        logger.error("Request Dump", extra={"details": log_details})

        return JSONResponse(
            status_code=e.status_code,
            content={
                "status_code": e.status_code,
                "is_error": True,
                "error_message": e.http_error,
            },
        )
    except Exception as e:
        internal_error = InternalServerError(str(e))
        log_details = {
            "status_code": internal_error.status_code,
            "error_message": str(internal_error),
            "method": request.method,
            "url": str(request.url),
            "headers": {
                key: value if key.lower() != "authorization" else "REDACTED"
                for key, value in request.headers.items()
            },
            "trace": traceback.format_exc(),
        }
        logger.error("Request Dump", extra={"details": log_details})
        return JSONResponse(
            status_code=internal_error.status_code,
            content={
                "status_code": internal_error.status_code,
                "is_error": True,
                "error_message": internal_error.http_error,
            },
        )
