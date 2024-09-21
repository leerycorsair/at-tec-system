from datetime import datetime
from os import name

from fastapi import Depends
from src.service.model.models.models import (
    CreateModelRequest,
    CreateModelResponse,
    GetModelResponse,
    GetModelsListResponse,
    ModelMeta,
    UpdateModelRequest,
)
from src.repository.model.models.models import CreateModelParamsDB, UpdateModelParamsDB
from src.repository.editor.function.repository import FunctionRepository
from src.repository.editor.resource.repository import ResourceRepository
from src.repository.editor.template.repository import TemplateRepository
from src.repository.model.repository import ModelRepository


class ModelService:
    def __init__(
        self,
        model_rep: ModelRepository = Depends(ModelRepository),
        resource_rep: ResourceRepository = Depends(ResourceRepository),  # service
        template_rep: TemplateRepository = Depends(TemplateRepository),  # service
        function_rep: FunctionRepository = Depends(FunctionRepository),  # service
    ):
        self._model_rep = model_rep
        self._resource_rep = resource_rep
        self._template_rep = template_rep
        self._function_rep = function_rep

    async def check_rights(self, model_id, user_id):
        model = await self._model_rep.get_model_short(model_id)
        if model.user_id != user_id:
            raise ValueError(f"User {user_id} doesn't owns model {model_id}")

    async def create_model(
        self, user_id: int, model: CreateModelRequest
    ) -> CreateModelResponse:
        new_model = await self._model_rep.create_model(
            CreateModelParamsDB(name=model.name, user_id=user_id)
        )
        return CreateModelResponse(
            id=new_model.id,
            name=new_model.name,
            created_at=new_model.created_at,
        )

    async def get_model(self, model_id: int) -> GetModelResponse:
        model_meta = await self._model_rep.get_model_short(model_id)
        return GetModelResponse(
            id=model_meta.id,
            name=model_meta.name,
            created_at=model_meta.created_at,
            resource_types=self._resource_rep.get_resource_types(model_id),
            resources=self._resource_rep.get_resources(model_id),
            functions=self._function_rep.get_functions(model_id),
            irregular_events=self._template_rep.get_irregular_event_templates(model_id),
            operations=self._template_rep.get_operation_templates(model_id),
            rules=self._template_rep.get_rule_templates(model_id),
            template_usages=self._template_rep.get_template_usages(model_id),
            # nodes
            # edges
        )

    async def get_models(self, user_id: int) -> GetModelsListResponse:
        models = await self._model_rep.get_models(user_id)
        return GetModelsListResponse(
            models=[
                ModelMeta(
                    id=model.id,
                    name=model.name,
                    created_at=model.created_at,
                )
                for model in models
            ],
            total=len(models),
        )

    async def update_model(
        self, model_id: int, params: UpdateModelRequest
    ) -> ModelMeta:
        model = await self._model_rep.update_model(
            model_id, UpdateModelParamsDB(name=params.name)
        )

        return ModelMeta(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
        )

    async def delete_model(self, model_id: int) -> int:
        return await self._model_rep.delete_model(model_id)
