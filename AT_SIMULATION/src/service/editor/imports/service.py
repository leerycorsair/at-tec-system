from typing import List

from src.repository.editor.imports.models.models import ImportDB
from src.service.editor.imports.dependencies import IImportRepository


class ImportService:
    def __init__(
        self,
        import_rep: IImportRepository,
    ) -> None:
        self._import_rep = import_rep

    def _check_import_rights(self, import_id: int, model_id: int) -> None:
        imp = self._import_rep.get_import(import_id)
        if imp.model_id != model_id:
            raise ValueError(f"Import {import_id} does not belong to model {model_id}")

    def create_import(self, imp: ImportDB) -> int:
        obj_id = self._import_rep.create_import(imp)

        return obj_id

    def get_import(self, import_id: int, model_id: int) -> ImportDB:
        self._check_import_rights(import_id, model_id)
        return self._import_rep.get_import(import_id)

    def get_imports(self, model_id: int) -> List[ImportDB]:
        return self._import_rep.get_imports(model_id)

    def update_import(self, imp: ImportDB) -> int:
        self._check_import_rights(imp.id, imp.model_id)
        obj_id = self._import_rep.update_import(imp)

        return obj_id

    def delete_import(self, import_id: int, model_id: int) -> int:
        self._check_import_rights(import_id, model_id)
        return self._import_rep.delete_import(import_id)
