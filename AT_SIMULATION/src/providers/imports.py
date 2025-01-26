from fastapi import Depends
from sqlalchemy.orm import Session

from src.repository.editor.imports.repository import ImportRepository
from src.service.editor.imports.service import ImportService
from src.storage.postgres.storage import get_db


def get_import_repository(session: Session = Depends(get_db)) -> ImportRepository:
    return ImportRepository(session)


def get_import_service(
    import_rep=Depends(get_import_repository),
) -> ImportService:
    return ImportService(import_rep)
