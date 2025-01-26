from fastapi import Depends

from src.repository.minio.repository import MinioRepository
from src.storage.minio.storage import get_minio_storage


def get_minio_repository(minio_info=Depends(get_minio_storage)) -> MinioRepository:
    client, bucket_name = minio_info
    return MinioRepository(client, bucket_name)
