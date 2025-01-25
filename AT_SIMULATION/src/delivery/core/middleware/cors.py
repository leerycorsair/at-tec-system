from typing import Awaitable, Callable

from fastapi import Request, Response


async def cors_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
):
    response = await call_next(request)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"

    if request.method == "OPTIONS":
        return Response(status_code=204)

    return response
