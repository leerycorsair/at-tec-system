from pydantic import BaseModel
from datetime import datetime


class FileMeta(BaseModel):
    user_id: int
    file_name: str
    model_id: int
    created_at: datetime

    def to_dict(self) -> dict:
        return {
            "user_id": str(self.user_id),
            "file_name": self.file_name,
            "model_id": str(self.model_id),
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_id=int(data["user_id"]),
            file_name=data["file_name"],
            model_id=data["model_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )


class MinioFile(BaseModel):
    minio_name: str
    last_modified: datetime
    size: int
    file_meta: FileMeta

    def to_dict(self) -> dict:
        return {
            "minio_name": self.minio_name,
            "last_modified": self.last_modified.isoformat(),
            "size": self.size,
            "file_meta": self.file_meta.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            minio_name=data["minio_name"],
            last_modified=datetime.fromisoformat(data["last_modified"]),
            size=data["size"],
            file_meta=FileMeta.from_dict(data["file_meta"]),
        )
