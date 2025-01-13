from typing import List
from src.repository.editor.imports.models.models import ImportDB, PackageDB
from src.schema.imports import Import, Package


def to_ImportDB(imp: Import, pkgs: List[Package]) -> ImportDB:
    return ImportDB(
        id=imp.id,
        name=imp.name,
        version=imp.version,
        model_id=imp.model_id,
        packages=[to_PackageDB(pkg) for pkg in pkgs],
    )


def to_PackageDB(pkg: Package) -> PackageDB:
    return PackageDB(
        id=pkg.id,
        name=pkg.name,
        alias=pkg.alias,
    )


def to_Import(imp: ImportDB) -> Import:
    return Import(
        name=imp.name,
        version=imp.version,
        model_id=imp.model_id,
    )


def to_Package(pkg: PackageDB, imp_id: int) -> Package:
    return Package(
        name=pkg.name,
        alias=pkg.alias,
        import_id=imp_id,
    )
