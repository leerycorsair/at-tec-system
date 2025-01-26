from fastapi import Depends
from sqlalchemy.orm import Session

from src.providers.visio import get_visio_service
from src.repository.editor.function.repository import FunctionRepository
from src.service.editor.function.service import FunctionService
from src.storage.postgres.storage import get_db


def get_function_repository(session: Session = Depends(get_db)) -> FunctionRepository:
    return FunctionRepository(session)


def get_function_service(
    function_rep=Depends(get_function_repository),
    visio_service=Depends(get_visio_service),
) -> FunctionService:
    return FunctionService(function_rep, visio_service)
