from typing import Protocol

from fastapi import Depends

from src.service.model.dependencies import (
    IModelRepository,
    get_function_service,
    get_model_repository,
    get_resource_service,
    get_template_service,
)
from src.service.model.models.models import Model
from src.service.model.service import ModelService


class IModelService(Protocol):
    def get_model(self, model_id: int, user_id: int) -> Model: ...


def get_model_service(
    model_rep: IModelRepository = Depends(get_model_repository),
    resource_service=Depends(get_resource_service),
    template_service=Depends(get_template_service),
    function_service=Depends(get_function_service),
) -> IModelService:
    return ModelService(
        model_rep,
        resource_service,
        template_service,
        function_service,
    )
