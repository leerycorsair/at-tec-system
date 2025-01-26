from typing import List, Protocol

from src.repository.editor.imports.models.models import ImportDB
from src.service.editor.imports.service import ImportService


class IImportService(Protocol):
    def create_import(self, imp: ImportDB) -> int: ...

    def get_import(self, import_id: int, model_id: int) -> ImportDB: ...

    def get_imports(self, model_id: int) -> List[ImportDB]: ...

    def update_import(self, imp: ImportDB) -> int: ...

    def delete_import(self, import_id: int, model_id: int) -> int: ...


_: IImportService = ImportService(...)  # type: ignore[arg-type, reportArgumentType]
