from fastapi import APIRouter, Depends
from src.delivery.model.dependencies import check_model_rights
from src.service.visio.models.models import MoveNodeRequest, UpdateNodeResponse
from src.service.visio.service import VisioService

router = APIRouter(
    prefix="/visio",
    tags=["visio"],
)


@router.put("/board/nodes/{node_id}/move", response_model=UpdateNodeResponse)
async def move_node(
    body: MoveNodeRequest,
    node_id: int = Depends(check_model_rights),
    visio_service: VisioService = Depends(),
) -> UpdateNodeResponse:
    return await visio_service.move_node(node_id, body)
