from fastapi import APIRouter, Depends
from src.delivery.core.models.conversions import InternalServiceError, SuccessResponse
from src.delivery.core.models.models import CommonResponse
from src.delivery.model.dependencies import get_current_model
from src.delivery.visio.dependencies import IVisioService, get_visio_service
from src.delivery.visio.models.conversions import to_EditorInfoResponse, to_MoveNodeDB
from src.delivery.visio.models.models import EditorInfoResponse, MoveNodeRequest

router = APIRouter(
    prefix="/visio",
    tags=["visio"],
)


@router.get("/editor/info", response_model=CommonResponse[EditorInfoResponse | None])
async def get_editor_info(
    model_id: int = Depends(get_current_model),
    visio_service: IVisioService = Depends(get_visio_service),
) -> CommonResponse[EditorInfoResponse]:
    try:
        return SuccessResponse(
            to_EditorInfoResponse(visio_service.get_editor_info(model_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.patch("/editor/nodes/{node_id}/move", response_model=CommonResponse[None])
async def move_node(
    body: MoveNodeRequest,
    node_id: int,
    model_id: int = Depends(get_current_model),
    visio_service: IVisioService = Depends(get_visio_service),
) -> CommonResponse[None]:
    try:
        visio_service.move_node(to_MoveNodeDB(body, node_id), model_id)
        return SuccessResponse(None)
    except Exception as e:
        return InternalServiceError(e)
