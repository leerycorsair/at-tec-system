from typing import List

from src.repository.editor.function.models.models import FunctionDB
from src.repository.editor.resource.models.models import ResourceDB, ResourceTypeDB
from src.repository.editor.template.models.models import TemplateUsageDB
from src.repository.model.models.models import ModelMetaDB
from src.service.editor.template.models.models import Templates
from src.service.model.models.models import Model


def to_Model(
    meta: ModelMetaDB,
    resource_types: List[ResourceTypeDB],
    resources: List[ResourceDB],
    templates: Templates,
    template_usages: List[TemplateUsageDB],
    functions: List[FunctionDB],
):
    return Model(
        meta=meta,
        resource_types=resource_types,
        resources=resources,
        irregular_events=templates.irregular_events,
        operations=templates.operations,
        rules=templates.rules,
        template_usages=template_usages,
        functions=functions,
    )
