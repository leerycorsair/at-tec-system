from abc import ABC, abstractmethod
from typing import List

from src.repository.editor.template.models.models import (
    IrregularEventDB,
    OperationDB,
    RuleDB,
    TemplateMetaDB,
    TemplateUsageDB,
)
from src.service.editor.template.service import TemplateService


class ITemplateService(ABC):
    @abstractmethod
    async def create_irregular_event(self, template: IrregularEventDB) -> int:
        pass

    @abstractmethod
    async def create_operation(self, template: OperationDB) -> int:
        pass

    @abstractmethod
    async def create_rule(self, template: RuleDB) -> int:
        pass

    @abstractmethod
    async def get_irregular_event(
        self, template_id: int, model_id: int
    ) -> IrregularEventDB:
        pass

    @abstractmethod
    async def get_operation(self, template_id: int, model_id: int) -> OperationDB:
        pass

    @abstractmethod
    async def get_rule(self, template_id: int, model_id: int) -> RuleDB:
        pass

    @abstractmethod
    async def update_irregular_event(self, template: IrregularEventDB) -> int:
        pass

    @abstractmethod
    async def update_operation(self, template: OperationDB) -> int:
        pass

    @abstractmethod
    async def update_rule(self, template: RuleDB) -> int:
        pass

    @abstractmethod
    async def get_templates(self, model_id: int) -> List[TemplateMetaDB]:
        pass

    @abstractmethod
    async def delete_template(self, template_id: int, model_id: int) -> int:
        pass

    @abstractmethod
    async def create_template_usage(self, template_usage: TemplateUsageDB) -> int:
        pass

    @abstractmethod
    async def get_template_usage(
        self, resource_type_id: int, model_id: int
    ) -> TemplateUsageDB:
        pass

    @abstractmethod
    async def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]:
        pass

    @abstractmethod
    async def update_template_usage(self, template_usage: TemplateUsageDB) -> int:
        pass

    @abstractmethod
    async def delete_template_usage(self, template_usage_id: int, model_id: int) -> int:
        pass


def get_template_service() -> ITemplateService:
    return TemplateService()
