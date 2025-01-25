from typing import List

from sqlalchemy.orm import Session

from src.repository.editor.imports.models.conversions import (
    to_Import,
    to_ImportDB,
    to_Package,
)
from src.repository.editor.imports.models.models import ImportDB
from src.repository.helper import handle_sqlalchemy_errors
from src.schema.imports import Import, Package


class ImportRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @handle_sqlalchemy_errors
    def create_import(self, imp: ImportDB) -> int:
        new_import = to_Import(imp)

        self.db_session.add(new_import)
        self.db_session.flush()

        new_import_pkgs = [to_Package(pkg, new_import.id) for pkg in imp.packages]

        self.db_session.add_all(new_import_pkgs)

        return new_import.id

    @handle_sqlalchemy_errors
    def get_import(self, import_id: int) -> ImportDB:
        imp = self._get_import_by_id(import_id)
        if not imp:
            raise RuntimeError("Import not found")
        pkgs = self._get_pkgs_by_import_id(import_id)
        return to_ImportDB(imp, pkgs)

    @handle_sqlalchemy_errors
    def get_imports(self, model_id: int) -> List[ImportDB]:
        imports = (
            self.db_session.query(Import).filter(Import.model_id == model_id).all()
        )

        imports_db = [
            to_ImportDB(imp, self._get_pkgs_by_import_id(imp.id)) for imp in imports
        ]
        return imports_db

    @handle_sqlalchemy_errors
    def update_import(self, imp: ImportDB) -> int:
        existing_import = self._get_import_by_id(imp.id)
        if not existing_import:
            raise RuntimeError("Import not found")

        existing_import.name = imp.name
        existing_import.version = imp.version
        existing_import.model_id = imp.model_id

        existing_pkgs = {
            pkg.id: pkg
            for pkg in self.db_session.query(Package)
            .filter(Package.import_id == imp.id)
            .all()
        }
        existing_pkg_ids = set(existing_pkgs.keys())

        for pkg in imp.packages:
            if pkg.id in existing_pkgs:
                existing_pkgs[pkg.id].name = pkg.name
                existing_pkgs[pkg.id].alias = pkg.alias
                existing_pkg_ids.remove(pkg.id)
            else:
                self.db_session.add(to_Package(pkg, imp.id))

        for pkg_id in existing_pkg_ids:
            pkg_to_delete = existing_pkgs[pkg_id]
            self.db_session.delete(pkg_to_delete)

        return imp.id

    @handle_sqlalchemy_errors
    def delete_import(self, import_id: int) -> int:
        imp = self._get_import_by_id(import_id)
        if not imp:
            raise RuntimeError("Import not found")
        self.db_session.delete(imp)

        return import_id

    def _get_import_by_id(self, import_id: int) -> Import:
        imp = self.db_session.query(Import).filter(Import.id == import_id).first()
        if not imp:
            raise ValueError("Import does not exist")
        return imp

    def _get_pkgs_by_import_id(self, import_id: int) -> List[Package]:
        return (
            self.db_session.query(Package).filter(Package.import_id == import_id).all()
        )
