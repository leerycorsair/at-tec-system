from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ...config.postgres import PostgresConfig
from typing import Generator


engine = create_engine(PostgresConfig.get_database_config().url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def dispose_engine():
    if engine:
        engine.dispose()
