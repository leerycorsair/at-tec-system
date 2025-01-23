import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from src.client.auth_client import AuthClientSingleton
from src.delivery.core.models.conversions import BadRequestError

from .delivery.router import setup_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_routes(app)
    # Initialize resources like database connections
    # setup_storage()

    auth_client = await AuthClientSingleton.get_instance()
    loop = asyncio.get_event_loop()
    task = loop.create_task(auth_client.start())

    yield
    # Cleanup resources
    # shutdown_storage()
    pass


app = FastAPI(title="AT_SIMULATION", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configure logging
logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error at {request.url}: {exc.errors()}", exc_info=True)

    # Prepare the response
    response_content = BadRequestError(exception=Exception("Invalid request body."))
    return JSONResponse(
        status_code=response_content.status_code,
        content=response_content.model_dump(),
    )
