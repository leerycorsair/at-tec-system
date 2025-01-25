from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config.postgres import PostgresStore

engine = create_engine(PostgresStore.get_database_config().url, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        if not db.is_active:
            return
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def dispose_engine():
    if engine:
        engine.dispose()
