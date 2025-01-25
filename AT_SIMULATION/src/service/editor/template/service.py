from typing import List

from src.repository.editor.template.models.models import (
    IrregularEventDB,
    OperationDB,
    RuleDB,
    TemplateTypeEnum,
    TemplateUsageDB,
)
from src.repository.visio.models.models import NodeTypesEnum
from src.service.editor.template.dependencies import ITemplateRepository, IVisioService
from src.service.editor.template.models.models import Templates
from src.service.helpers import handle_rollback


class TemplateService:
    _template_nodes = {
        TemplateTypeEnum.IRREGULAR_EVENT: NodeTypesEnum.IRREGULAR_EVENT_T,
        TemplateTypeEnum.OPERATION: NodeTypesEnum.OPERATION_T,
        TemplateTypeEnum.RULE: NodeTypesEnum.RULE_T,
    }

    _usage_nodes = {
        TemplateTypeEnum.IRREGULAR_EVENT: NodeTypesEnum.IRREGULAR_EVENT_U,
        TemplateTypeEnum.OPERATION: NodeTypesEnum.OPERATION_U,
        TemplateTypeEnum.RULE: NodeTypesEnum.RULE_U,
    }

    def __init__(
        self,
        template_rep: ITemplateRepository,
        visio_service: IVisioService,
    ) -> None:
        self._template_rep = template_rep
        self._visio_service = visio_service

    def create_irregular_event(self, template: IrregularEventDB) -> int:
        return self._create_template(
            self._template_rep.create_irregular_event,
            template,
        )

    def create_operation(self, template: OperationDB) -> int:
        return self._create_template(
            self._template_rep.create_operation,
            template,
        )

    def create_rule(self, template: RuleDB) -> int:
        return self._create_template(
            self._template_rep.create_rule,
            template,
        )

    def get_irregular_event(self, template_id: int, model_id: int) -> IrregularEventDB:
        self._check_template_rights(template_id, model_id)
        return self._template_rep.get_irregular_event(template_id)

    def get_operation(self, template_id: int, model_id: int) -> OperationDB:
        self._check_template_rights(template_id, model_id)
        return self._template_rep.get_operation(template_id)

    def get_rule(self, template_id: int, model_id: int) -> RuleDB:
        self._check_template_rights(template_id, model_id)
        return self._template_rep.get_rule(template_id)

    def update_irregular_event(self, template: IrregularEventDB) -> int:
        return self._update_template(
            template,
            self._template_rep.get_irregular_event,
            self._template_rep.update_irregular_event,
        )

    def update_operation(self, template: OperationDB) -> int:
        return self._update_template(
            template,
            self._template_rep.get_operation,
            self._template_rep.update_operation,
        )

    def update_rule(self, template: RuleDB) -> int:
        return self._update_template(
            template,
            self._template_rep.get_rule,
            self._template_rep.update_rule,
        )

    def get_templates(self, model_id: int) -> Templates:
        return Templates(
            irregular_events=self._template_rep.get_irregular_events(model_id),
            operations=self._template_rep.get_operations(model_id),
            rules=self._template_rep.get_rules(model_id),
        )

    def delete_template(self, template_id: int, model_id: int) -> int:
        self._check_template_rights(template_id, model_id)
        return self._template_rep.delete_template(template_id)

    def create_template_usage(self, template_usage: TemplateUsageDB) -> int:
        obj_id = self._template_rep.create_template_usage(template_usage)

        template_meta = self._template_rep.get_template_meta(template_usage.template_id)
        with handle_rollback(self._template_rep.delete_template_usage, obj_id):
            usage_node_id = self._visio_service.create_node(
                obj_id,
                template_usage.name,
                self._usage_nodes.get(template_meta.type),
                template_usage.model_id,
            )

        template_meta = self._template_rep.get_template_meta(template_usage.template_id)
        template_node = self._visio_service.get_node(
            template_meta.id, self._template_nodes.get(template_meta.type)
        )

        with handle_rollback(self._visio_service.delete_node, obj_id, usage_node_id):
            with handle_rollback(self._template_rep.delete_template_usage, obj_id):
                self._visio_service.create_edge(
                    template_node.id, usage_node_id, template_usage.model_id
                )

        for argument in template_usage.arguments:
            with handle_rollback(self._template_rep.delete_template_usage, obj_id):
                resource_node = self._visio_service.get_node(
                    argument.resource_id, NodeTypesEnum.RESOURCE
                )
                self._visio_service.create_edge(
                    usage_node_id, resource_node.id, template_usage.model_id
                )

        return obj_id

    def get_template_usage(
        self, template_usage_id: int, model_id: int
    ) -> TemplateUsageDB:
        self._check_template_usage_rights(template_usage_id, model_id)
        return self._template_rep.get_template_usage(template_usage_id)

    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]:
        return self._template_rep.get_template_usages(model_id)

    def update_template_usage(self, template_usage: TemplateUsageDB) -> int:
        self._check_template_usage_rights(template_usage.id, template_usage.model_id)
        original_template_usage = self._template_rep.get_template_usage(
            template_usage.id
        )
        obj_id = self._template_rep.update_template_usage(template_usage)

        template_meta = self._template_rep.get_template_meta(template_usage.template_id)
        with handle_rollback(
            self._template_rep.update_template_usage, original_template_usage
        ):
            self._visio_service.update_node_name(
                obj_id, template_usage.name, self._usage_nodes.get(template_meta.type)
            )

        return obj_id

    def delete_template_usage(self, template_usage_id: int, model_id: int) -> int:
        self._check_template_usage_rights(template_usage_id, model_id)
        return self._template_rep.delete_template_usage(template_usage_id)

    def _update_template(
        self,
        template: IrregularEventDB | OperationDB | RuleDB,
        get_func,
        update_func,
    ) -> int:
        self._check_template_rights(template.meta.id, template.meta.model_id)
        original_template = get_func(template.meta.id)
        obj_id = update_func(template)

        with handle_rollback(update_func, original_template):
            self._visio_service.update_node_name(
                obj_id, template.meta.name, self._template_nodes.get(template.meta.type)
            )

        return obj_id

    def _check_template_rights(self, template_id: int, model_id: int) -> None:
        template_meta = self._template_rep.get_template_meta(template_id)
        if template_meta.model_id != model_id:
            raise ValueError(
                f"Template {template_id} does not belong to model {model_id}"
            )

    def _check_template_usage_rights(self, usage_id: int, model_id: int) -> None:
        template_usage = self._template_rep.get_template_usage(usage_id)
        if template_usage.model_id != model_id:
            raise ValueError(
                f"Template usage {usage_id} does not belong to model {model_id}"
            )

    def _create_template(
        self,
        create_func,
        template: IrregularEventDB | OperationDB | RuleDB,
    ) -> int:
        obj_id = create_func(template)

        with handle_rollback(self._template_rep.delete_template, obj_id):
            self._visio_service.create_node(
                obj_id,
                template.meta.name,
                self._template_nodes.get(template.meta.type),
                template.meta.model_id,
            )

        return obj_id
