from typing import List, Protocol

from fastapi import Depends
from src.repository.editor.imports.models.models import ImportDB
from src.service.editor.imports.dependencies import get_import_repository
from src.service.editor.imports.service import ImportService


class IImportService(Protocol):
    def create_import(self, imp: ImportDB) -> int: ...

    def get_import(self, import_id: int, model_id: int) -> ImportDB: ...

    def get_imports(self, model_id: int) -> List[ImportDB]: ...

    def update_import(self, imp: ImportDB) -> int: ...

    def delete_import(self, import_id: int, model_id: int) -> int: ...


def get_import_service(
    import_rep=Depends(get_import_repository),
) -> IImportService:
    return ImportService(import_rep)
