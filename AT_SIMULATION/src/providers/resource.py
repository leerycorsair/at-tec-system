from fastapi import Depends
from sqlalchemy.orm import Session

from src.providers.visio import get_visio_service
from src.repository.editor.resource.repository import ResourceRepository
from src.service.editor.resource.service import ResourceService
from src.storage.postgres.storage import get_db


def get_resource_repository(session: Session = Depends(get_db)) -> ResourceRepository:
    return ResourceRepository(session)


def get_resource_service(
    resource_rep=Depends(get_resource_repository),
    visio_service=Depends(get_visio_service),
) -> ResourceService:
    return ResourceService(resource_rep, visio_service)
