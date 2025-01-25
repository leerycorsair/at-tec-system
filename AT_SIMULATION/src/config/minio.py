import os
from dataclasses import dataclass


@dataclass
class MinioConfig:
    endpoint: str
    access_key: str
    secret_key: str
    secure: bool
    bucket_name: str
    api_port: int
    console_port: int


class MinioStore:

    @classmethod
    def get_minio_config(cls) -> MinioConfig:
        MINIO_HOST = os.getenv("MINIO_HOST", "play.min.io").strip()
        MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "your-access-key").strip()
        MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "your-secret-key").strip()
        MINIO_SECURE = os.getenv("MINIO_SECURE", "true").lower() == "true"
        MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "my-bucket").strip()
        MINIO_API_PORT = int(os.getenv("MINIO_API_PORT", "9000"))
        MINIO_CONSOLE_PORT = int(os.getenv("MINIO_CONSOLE_PORT", "9001"))
        
        endpoint = f"{MINIO_HOST}:{MINIO_API_PORT}"

        return MinioConfig(
            endpoint=endpoint,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE,
            bucket_name=MINIO_BUCKET_NAME,
            api_port=MINIO_API_PORT,
            console_port=MINIO_CONSOLE_PORT,
        )
