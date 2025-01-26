from typing import Protocol

from src.repository.visio.models.models import EditorInfoDB, MoveNodeDB
from src.service.visio.service import VisioService


class IVisioService(Protocol):
    def get_editor_info(self, model_id: int) -> EditorInfoDB: ...

    def move_node(self, params: MoveNodeDB, model_id: int) -> None: ...


_: IVisioService = VisioService(...)  # type: ignore[arg-type, reportArgumentType]
