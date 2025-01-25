from typing import List, Protocol

from fastapi import Depends

from src.repository.editor.template.models.models import (
    IrregularEventDB,
    OperationDB,
    RuleDB,
    TemplateUsageDB,
)
from src.service.editor.template.dependencies import (
    get_template_repository,
    get_visio_service,
)
from src.service.editor.template.models.models import Templates
from src.service.editor.template.service import TemplateService


class ITemplateService(Protocol):
    def create_irregular_event(self, template: IrregularEventDB) -> int: ...

    def create_operation(self, template: OperationDB) -> int: ...

    def create_rule(self, template: RuleDB) -> int: ...

    def get_irregular_event(
        self, template_id: int, model_id: int
    ) -> IrregularEventDB: ...

    def get_operation(self, template_id: int, model_id: int) -> OperationDB: ...

    def get_rule(self, template_id: int, model_id: int) -> RuleDB: ...

    def update_irregular_event(self, template: IrregularEventDB) -> int: ...

    def update_operation(self, template: OperationDB) -> int: ...

    def update_rule(self, template: RuleDB) -> int: ...

    def get_templates(self, model_id: int) -> Templates: ...

    def delete_template(self, template_id: int, model_id: int) -> int: ...

    def create_template_usage(self, template_usage: TemplateUsageDB) -> int: ...

    def get_template_usage(
        self, template_usage_id: int, model_id: int
    ) -> TemplateUsageDB: ...

    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]: ...

    def update_template_usage(self, template_usage: TemplateUsageDB) -> int: ...

    def delete_template_usage(self, template_usage_id: int, model_id: int) -> int: ...


def get_template_service(
    template_rep=Depends(get_template_repository),
    visio_service=Depends(get_visio_service),
) -> ITemplateService:
    return TemplateService(template_rep, visio_service)
