from time import time
from minio import Minio


class MinioRepository:
    def __init__(self, minio_client: Minio, bucket_name: str):
        self._minio_client = minio_client
        self._bucket_name = bucket_name

    def load_file(
        self, user_id: int, file_path: str, file_name: str, model_name: str
    ) -> str:
        timestamp = int(time())
        minio_file_name = f"{file_name}_{model_name}_{timestamp}"
        metadata = {
            "user_id": str(user_id),
            "file_name": file_name,
            "model_name": model_name,
            "timestamp": str(timestamp),
        }

        self._minio_client.fput_object(
            self._bucket_name,
            minio_file_name,
            file_path,
            metadata=metadata,
        )

        return minio_file_name
