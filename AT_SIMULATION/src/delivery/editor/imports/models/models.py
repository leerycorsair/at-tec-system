from typing import List, Optional, Sequence

from pydantic import BaseModel


class PackageRequest(BaseModel):
    id: Optional[int] = None
    name: str
    alias: str


class ImportRequest(BaseModel):
    id: Optional[int] = None
    name: str
    version: str
    pkgs: Sequence[PackageRequest]


class PackageResponse(PackageRequest):
    id: int


class ImportResponse(ImportRequest):
    id: int
    pkgs: Sequence[PackageResponse]


class ImportsResponse(BaseModel):
    imports: List[ImportResponse]
    total: int
