from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from .frontend import frontend_router, FRONTEND_BUILD_PATH
from .auth_router import router as auth_router

import os

_router = APIRouter (
    prefix="/api",
)

def setup_routes(app: FastAPI):
    _router.include_router(auth_router)
    app.include_router(_router)
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_BUILD_PATH, "static")), name="static")
    app.include_router(frontend_router)
    