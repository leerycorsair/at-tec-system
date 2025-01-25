from typing import Protocol

from fastapi import Depends

from src.repository.visio.models.models import EditorInfoDB, MoveNodeDB
from src.service.visio.dependencies import get_visio_repository
from src.service.visio.service import VisioService


class IVisioService(Protocol):
    def get_editor_info(self, model_id: int) -> EditorInfoDB: ...

    def move_node(self, params: MoveNodeDB, model_id: int) -> None: ...


def get_visio_service(
    visio_rep=Depends(get_visio_repository),
) -> IVisioService:
    return VisioService(visio_rep)
