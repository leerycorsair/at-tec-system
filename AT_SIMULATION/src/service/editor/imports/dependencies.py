from typing import List, Protocol

from fastapi import Depends

from sqlalchemy.orm import Session
from src.repository.editor.imports.models.models import ImportDB
from src.repository.editor.imports.repository import ImportRepository
from src.storage.postgres.session import get_db


class IImportRepository(Protocol):
    def create_import(self, imp: ImportDB) -> int: ...

    def get_import(self, import_id: int) -> ImportDB: ...

    def get_imports(self, model_id: int) -> List[ImportDB]: ...

    def update_import(self, imp: ImportDB) -> int: ...

    def delete_import(self, import_id: int) -> int: ...


def get_import_repository(session: Session = Depends(get_db)) -> IImportRepository:
    return ImportRepository(session)
