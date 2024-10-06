from fastapi import APIRouter, Depends
from src.service.visio.models.models import MoveNodeRequest, UpdateNodeResponse
from src.service.visio.service import VisioService

router = APIRouter(
    prefix="/visio",
    tags=["visio"],
)


@router.put("/board/nodes/{node_id}/move", response_model=UpdateNodeResponse)
async def move_node(
    body: MoveNodeRequest,
    node_id: int = 10,
    visio_service: VisioService = Depends(),
) -> UpdateNodeResponse:
    return await visio_service.move_node(node_id, body)
