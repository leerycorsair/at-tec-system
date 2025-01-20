from datetime import datetime
from typing import List
from minio import Minio, S3Error
import uuid

from src.repository.minio.models.models import FileMeta, MinioFile


class MinioRepository:
    def __init__(self, minio_client: Minio, bucket_name: str):
        self._minio_client = minio_client
        self._bucket_name = bucket_name

    def load_file(
        self, user_id: int, file_path: str, file_name: str, model_id: int
    ) -> str:
        timestamp = datetime.now()
        minio_file_name = f"{uuid.uuid4()}"

        meta_data = FileMeta(
            user_id=user_id,
            file_name=file_name,
            model_id=model_id,
            created_at=timestamp,
        )

        self._minio_client.fput_object(
            self._bucket_name,
            minio_file_name,
            file_path,
            metadata=meta_data.to_dict(),
        )

        return minio_file_name

    def get_files(self, user_id: int) -> List[MinioFile]:
        user_files: List[MinioFile] = []

        try:
            objects = self._minio_client.list_objects(self._bucket_name, recursive=True)
            for obj in objects:
                obj_metadata = self._minio_client.stat_object(
                    self._bucket_name,
                    obj.object_name,
                )

                if obj_metadata.metadata.get("x-amz-meta-user_id") == str(user_id):
                    file_meta = FileMeta(
                        user_id=int(obj_metadata.metadata.get("x-amz-meta-user_id")),
                        file_name=obj_metadata.metadata.get("x-amz-meta-file_name"),
                        model_id=obj_metadata.metadata.get("x-amz-meta-model_id"),
                        created_at=datetime.fromisoformat(
                            obj_metadata.metadata.get("x-amz-meta-created_at")
                        ),
                    )

                    user_files.append(
                        MinioFile(
                            minio_name=obj.object_name,
                            last_modified=obj.last_modified,
                            size=obj.size,
                            file_meta=file_meta,
                        )
                    )
        except S3Error as e:
            raise S3Error(f"Error retrieving files: {e}")

        return user_files
