from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config.postgres import PostgresStore
from typing import Generator


engine = create_engine(PostgresStore.get_database_config().url, echo=False)
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
