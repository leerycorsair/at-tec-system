from fastapi import APIRouter

from .function.router import function_router

router = APIRouter(
    prefix="/editor",
)

# router.include_router(resource_router)
# router.include_router(template_router)
# router.include_router(function_router)
