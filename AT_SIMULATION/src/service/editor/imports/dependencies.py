from typing import List, Protocol

from src.repository.editor.imports.models.models import ImportDB
from src.repository.editor.imports.repository import ImportRepository


class IImportRepository(Protocol):
    def create_import(self, imp: ImportDB) -> int: ...

    def get_import(self, import_id: int) -> ImportDB: ...

    def get_imports(self, model_id: int) -> List[ImportDB]: ...

    def update_import(self, imp: ImportDB) -> int: ...

    def delete_import(self, import_id: int) -> int: ...


_: IImportRepository = ImportRepository(...)  # type: ignore[arg-type, reportArgumentType]
