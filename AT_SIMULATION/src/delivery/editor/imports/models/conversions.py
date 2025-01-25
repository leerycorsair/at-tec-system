from typing import List

from src.delivery.editor.imports.models.models import (ImportRequest,
                                                       ImportResponse,
                                                       ImportsResponse,
                                                       PackageRequest,
                                                       PackageResponse)
from src.repository.editor.imports.models.models import ImportDB, PackageDB


def to_PackageDB(
    pkg: PackageRequest,
    import_id: int,
) -> PackageDB:
    return PackageDB(
        id=pkg.id or 0,
        name=pkg.name,
        alias=pkg.alias,
        import_id=import_id,
    )


def to_ImportDB(
    imp: ImportRequest,
    model_id: int,
) -> ImportDB:
    return ImportDB(
        id=imp.id or 0,
        name=imp.name,
        version=imp.version,
        model_id=model_id,
        packages=[to_PackageDB(pkg, imp.id or 0) for pkg in imp.pkgs],
    )


def to_PackageResponse(
    pkg: PackageDB,
) -> PackageResponse:
    return PackageResponse(
        id=pkg.id,
        name=pkg.name,
        alias=pkg.alias,
    )


def to_ImportResponse(imp: ImportDB) -> ImportResponse:
    return ImportResponse(
        id=imp.id,
        name=imp.name,
        version=imp.version,
        pkgs=[to_PackageResponse(pkg) for pkg in imp.packages],
    )


def to_ImportsResponse(imports: List[ImportDB]) -> ImportsResponse:
    return ImportsResponse(
        imports=[to_ImportResponse(imp) for imp in imports],
        total=len(imports),
    )
