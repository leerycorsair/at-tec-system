from typing import List, Protocol
from src.repository.editor.template.models.models import (
    IrregularEventDB,
    OperationDB,
    RuleDB,
    TemplateMetaDB,
    TemplateUsageDB,
)
from src.repository.editor.template.repository import TemplateRepository
from src.service.visio.service import VisioService


class ITemplateRepository(Protocol):
    def create_irregular_event(self, template: IrregularEventDB) -> int: ...

    def create_operation(self, template: OperationDB) -> int: ...

    def create_rule(self, template: RuleDB) -> int: ...

    def get_irregular_event(self, template_id: int) -> IrregularEventDB: ...

    def get_operation(self, template_id: int) -> OperationDB: ...

    def get_rule(self, template_id: int) -> RuleDB: ...

    def update_irregular_event(self, template: IrregularEventDB) -> int: ...

    def update_operation(self, template: OperationDB) -> int: ...

    def update_rule(self, template: RuleDB) -> int: ...

    def get_irregular_events(self, model_id: int) -> List[IrregularEventDB]: ...

    def get_operations(self, model_id: int) -> List[OperationDB]: ...

    def get_rules(self, model_id: int) -> List[RuleDB]: ...

    def get_template_meta(self, template_id: int) -> TemplateMetaDB: ...

    def delete_template(self, template_id: int) -> int: ...

    def create_template_usage(self, template_usage: TemplateUsageDB) -> int: ...

    def get_template_usage(self, template_usage_id: int) -> TemplateUsageDB: ...

    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]: ...

    def update_template_usage(self, template_usage: TemplateUsageDB) -> int: ...

    def delete_template_usage(self, template_usage_id: int) -> int: ...


def get_template_repository() -> ITemplateRepository:
    return TemplateRepository()


class IVisioService(Protocol):
    def create_node(
        self,
        object_id: int,
        object_type: str,
        object_name: str,
        model_id: int,
    ) -> int: ...

    def update_node(
        self,
        object_id: int,
        object_type: str,
        object_name: str,
    ) -> None: ...

    def get_node_id(self, object_id: int, object_type: str) -> int: ...

    def delete_node(
        self,
        object_id: int,
        object_type: str,
    ) -> None: ...

    def create_edge(
        self,
        from_id: int,
        to_id: int,
        model_id: int,
    ) -> None: ...


def get_visio_service() -> IVisioService:
    return VisioService()
