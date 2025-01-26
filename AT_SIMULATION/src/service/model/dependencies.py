from typing import List, Protocol

from src.repository.editor.function.models.models import FunctionDB
from src.repository.editor.resource.models.models import ResourceDB, ResourceTypeDB
from src.repository.editor.template.models.models import TemplateUsageDB
from src.repository.model.models.models import ModelMetaDB
from src.repository.model.repository import ModelRepository
from src.service.editor.function.service import FunctionService
from src.service.editor.resource.service import ResourceService
from src.service.editor.template.models.models import Templates
from src.service.editor.template.service import TemplateService


class IModelRepository(Protocol):
    def create_model(self, model: ModelMetaDB) -> int: ...

    def get_model_meta(self, model_id: int) -> ModelMetaDB: ...

    def get_models(self, user_id: int) -> List[ModelMetaDB]: ...

    def update_model(self, model: ModelMetaDB) -> int: ...

    def delete_model(self, model_id: int) -> int: ...


_: IModelRepository = ModelRepository(...)  # type: ignore[arg-type, reportArgumentType]


class IResourceService(Protocol):
    def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]: ...

    def get_resources(self, model_id: int) -> List[ResourceDB]: ...


_: IResourceService = ResourceService(..., ...)  # type: ignore[arg-type, reportArgumentType]


class IFunctionService(Protocol):
    def get_functions(self, model_id: int) -> List[FunctionDB]: ...


_: IFunctionService = FunctionService(..., ...)  # type: ignore[arg-type, reportArgumentType]


class ITemplateService(Protocol):
    def get_templates(self, model_id: int) -> Templates: ...

    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]: ...


_: ITemplateService = TemplateService(..., ...)  # type: ignore[arg-type, reportArgumentType]
