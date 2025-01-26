from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    host: str = Field("localhost", alias="DB_HOST")
    port: int = Field(5432, alias="DB_PORT")
    name: str = Field("postgres", alias="DB_NAME")
    user: str = Field("postgres", alias="DB_USER")
    password: str = Field("password", alias="DB_PASS")

    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class PostgresStore:
    @classmethod
    @lru_cache(maxsize=1)
    def get_database_config(cls) -> DatabaseConfig:
        return DatabaseConfig()
