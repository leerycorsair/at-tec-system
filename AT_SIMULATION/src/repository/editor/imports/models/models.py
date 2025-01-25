from typing import List

from pydantic import BaseModel


class PackageDB(BaseModel):
    id: int
    name: str
    alias: str
    import_id: int


class ImportDB(BaseModel):
    id: int
    name: str
    version: str
    model_id: int
    packages: List[PackageDB]
