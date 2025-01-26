from fastapi import Depends
from sqlalchemy.orm import Session

from src.repository.visio.repository import VisioRepository
from src.service.visio.service import VisioService
from src.storage.postgres.storage import get_db


def get_visio_repository(session: Session = Depends(get_db)) -> VisioRepository:
    return VisioRepository(session)


def get_visio_service(visio_rep=Depends(get_visio_repository)) -> VisioService:
    return VisioService(visio_rep)
