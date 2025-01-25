from fastapi import APIRouter

from src.delivery.editor.function.router import router as function_router
from src.delivery.editor.imports.router import router as import_router
from src.delivery.editor.resource.router import router as resource_router
from src.delivery.editor.template.router import router as template_router

router = APIRouter(
    prefix="/editor",
)

router.include_router(resource_router)
router.include_router(template_router)
router.include_router(function_router)
router.include_router(import_router)
