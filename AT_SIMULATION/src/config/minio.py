from dataclasses import dataclass
import os


@dataclass
class MinioConfig:
    endpoint: str
    access_key: str
    secret_key: str
    secure: bool
    bucket_name: str


class MinioStore:

    @classmethod
    def get_minio_config(cls) -> MinioConfig:
        MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "play.min.io").strip()
        MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "your-access-key").strip()
        MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "your-secret-key").strip()
        MINIO_SECURE = os.getenv("MINIO_SECURE", "true").lower() == "true"
        MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "my-bucket").strip()

        return MinioConfig(
            endpoint=MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE,
            bucket_name=MINIO_BUCKET_NAME,
        )
