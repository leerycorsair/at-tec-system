import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: str
    name: str
    user: str
    password: str
    url: str


class PostgresStore:

    @classmethod
    def get_database_config(cls) -> DatabaseConfig:
        DB_HOST = os.getenv("DB_HOST", "localhost").strip()
        DB_PORT = os.getenv("DB_PORT", "5432").strip()
        DB_NAME = os.getenv("DB_NAME", "postgres").strip()
        DB_USER = os.getenv("DB_USER", "postgres").strip()
        DB_PASS = os.getenv("DB_PASS", "password").strip()

        database_url = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        return DatabaseConfig(
            host=DB_HOST,
            port=DB_PORT,
            name=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            url=database_url,
        )
