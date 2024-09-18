from fastapi import Depends

from src.delivery.model.dependencies import check_model_rights
from src.service.visio.visio import VisioService


async def check_node_rights(
    node_id: int,
    model_id: int = Depends(check_model_rights),
    visio_service: VisioService = Depends(),
):
    await visio_service.check_rights(node_id, model_id)
