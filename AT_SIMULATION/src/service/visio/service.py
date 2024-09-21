from src.service.visio.models.models import (
    MoveNodeRequest,
    UpdateNodeResponse,
)


class VisioService:

    async def move_node(
        self, node_id: int, params: MoveNodeRequest
    ) -> UpdateNodeResponse:
        pass

    async def check_rights(self, node_id: int, model_id: int) -> None:
        pass
