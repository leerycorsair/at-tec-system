from fastapi import APIRouter, FastAPI


from .editor.router import router as editor_router
from .model.router import router as model_router
from .visio.router import router as visio_router

_router = APIRouter(
    prefix="/api",
)


def setup_routes(app: FastAPI):
    _router.include_router(editor_router)
    _router.include_router(model_router)
    _router.include_router(visio_router)
    app.include_router(_router)
