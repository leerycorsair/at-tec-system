from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class MinioConfig(BaseSettings):
    host: str = Field("play.min.io", alias="MINIO_HOST")
    access_key: str = Field("your-access-key", alias="MINIO_ACCESS_KEY")
    secret_key: str = Field("your-secret-key", alias="MINIO_SECRET_KEY")
    secure: bool = Field(True, alias="MINIO_SECURE")
    bucket_name: str = Field("my-bucket", alias="MINIO_BUCKET_NAME")
    api_port: int = Field(9000, alias="MINIO_API_PORT")
    console_port: int = Field(9001, alias="MINIO_CONSOLE_PORT")

    @property
    def endpoint(self) -> str:
        return f"{self.host}:{self.api_port}"


class MinioStore:
    @classmethod
    @lru_cache(maxsize=1)
    def get_minio_config(cls) -> MinioConfig:
        return MinioConfig()
