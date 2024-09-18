from fastapi import APIRouter, FastAPI


from .auth_router import router as auth_router

_router = APIRouter (
    prefix="/api",
)

def setup_routes(app: FastAPI):
    _router.include_router(auth_router)
    app.include_router(_router)