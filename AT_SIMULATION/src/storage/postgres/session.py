from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config.postgres import PostgresStore
from typing import Generator
from contextlib import contextmanager


engine = create_engine(PostgresStore.get_database_config().url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def session_scope(session: Session):
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def dispose_engine():
    if engine:
        engine.dispose()
