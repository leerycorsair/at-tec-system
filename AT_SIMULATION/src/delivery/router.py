from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
import os

from .editor.router import router as editor_router
from .model.router import router as model_router
from .visio.router import router as visio_router
from .frontend import frontend_router, FRONTEND_BUILD_PATH

_router = APIRouter(
    prefix="/api",
)


def setup_routes(app: FastAPI):
    _router.include_router(editor_router)
    _router.include_router(model_router)
    _router.include_router(visio_router)
    app.include_router(_router)
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_BUILD_PATH, "static")), name="static")
    app.include_router(frontend_router)
