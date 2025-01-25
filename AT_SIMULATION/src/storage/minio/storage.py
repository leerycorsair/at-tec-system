from typing import Tuple

from minio import Minio

from src.config.minio import MinioStore


def get_minio_storage() -> Tuple[Minio, str]:
    config = MinioStore.get_minio_config()
    client = Minio(
        config.endpoint,
        access_key=config.access_key,
        secret_key=config.secret_key,
        secure=config.secure,
    )

    if not client.bucket_exists(config.bucket_name):
        client.make_bucket(config.bucket_name)

    return client, config.bucket_name
