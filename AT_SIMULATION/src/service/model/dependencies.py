from typing import List, Protocol

from fastapi import Depends
from sqlalchemy.orm import Session

from src.delivery.visio.dependencies import get_visio_service
from src.repository.editor.function.models.models import FunctionDB
from src.repository.editor.resource.models.models import (ResourceDB,
                                                          ResourceTypeDB)
from src.repository.editor.template.models.models import TemplateUsageDB
from src.repository.model.models.models import ModelMetaDB
from src.repository.model.repository import ModelRepository
from src.service.editor.function.dependencies import get_function_repository
from src.service.editor.function.service import FunctionService
from src.service.editor.resource.dependencies import get_resource_repository
from src.service.editor.resource.service import ResourceService
from src.service.editor.template.dependencies import get_template_repository
from src.service.editor.template.models.models import Templates
from src.service.editor.template.service import TemplateService
from src.storage.postgres.storage import get_db


class IModelRepository(Protocol):
    def create_model(self, model: ModelMetaDB) -> int: ...

    def get_model_meta(self, model_id: int) -> ModelMetaDB: ...

    def get_models(self, user_id: int) -> List[ModelMetaDB]: ...

    def update_model(self, model: ModelMetaDB) -> int: ...

    def delete_model(self, model_id: int) -> int: ...


class IResourceService(Protocol):
    def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]: ...

    def get_resources(self, model_id: int) -> List[ResourceDB]: ...


class IFunctionService(Protocol):
    def get_functions(self, model_id: int) -> List[FunctionDB]: ...


class ITemplateService(Protocol):
    def get_templates(self, model_id: int) -> Templates: ...

    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]: ...


def get_template_service(
    template_rep=Depends(get_template_repository),
    visio_service=Depends(get_visio_service),
) -> ITemplateService:
    return TemplateService(template_rep, visio_service)


def get_function_service(
    function_rep=Depends(get_function_repository),
    visio_service=Depends(get_visio_service),
) -> IFunctionService:
    return FunctionService(function_rep, visio_service)


def get_resource_service(
    resource_rep=Depends(get_resource_repository),
    visio_service=Depends(get_visio_service),
) -> IResourceService:
    return ResourceService(resource_rep, visio_service)


def get_model_repository(session: Session = Depends(get_db)) -> IModelRepository:
    return ModelRepository(session)
