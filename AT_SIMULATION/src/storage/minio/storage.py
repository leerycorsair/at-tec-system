from minio import Minio
from src.config.minio import MinioStore


def get_file_storage():
    config = MinioStore.get_minio_config()
    client = Minio(
        config.endpoint,
        access_key=config.access_key,
        secret_key=config.secret_key,
        secure=config.secure,
    )

    if not client.bucket_exists(config.bucket_name):
        client.make_bucket(config.bucket_name)

    return client
