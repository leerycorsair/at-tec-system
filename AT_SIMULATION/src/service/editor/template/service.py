from typing import Any, Callable, Dict, List, Union
from fastapi import Depends
from src.repository.editor.template.models.models import (
    IrregularEventDB,
    OperationDB,
    RuleDB,
    TemplateUsageDB,
)
from src.service.editor.template.dependencies import (
    ITemplateRepository,
    IVisioService,
    get_template_repository,
    get_visio_service,
)
from src.service.editor.template.models.models import Templates
from src.service.helpers import handle_rollback

_irregular_event_prefix = "irregular_event"
_operation_prefix = "operation"
_rule_prefix = "rule"
_template_usage_prefix = "template_usage"
_resource_prefix = "resource"


class TemplateService:
    _node_prefixes: Dict[str, str] = {
        "irregular_event": "irregular_event",
        "operation": "operation",
        "rule": "rule",
    }

    def __init__(
        self,
        template_rep: ITemplateRepository = Depends(get_template_repository),
        visio_service: IVisioService = Depends(get_visio_service),
    ) -> None:
        self._template_rep = template_rep
        self._visio_service = visio_service

    def _check_template_rights(self, template_id: int, model_id: int) -> None:
        template_meta = self._template_rep.get_template_meta(template_id)
        if template_meta.id != model_id:
            raise ValueError(
                f"Template {template_id} does not belong to model {model_id}"
            )

    def _check_template_usage_rights(self, usage_id: int, model_id: int) -> None:
        template_usage = self._template_rep.get_template_usage(usage_id)
        if template_usage.id != model_id:
            raise ValueError(
                f"Template usage {usage_id} does not belong to model {model_id}"
            )

    def _create_template(
        self,
        create_func,
        template: IrregularEventDB | OperationDB | RuleDB,
        node_prefix: str,
    ) -> int:
        obj_id = create_func(template)

        with handle_rollback(self._template_rep.delete_template, obj_id):
            self._visio_service.create_node(
                obj_id,
                node_prefix,
                template.meta.name,
                template.meta.model_id,
            )

        return obj_id

    def create_irregular_event(self, template: IrregularEventDB) -> int:
        return self._create_template(
            self._template_rep.create_irregular_event, template, _irregular_event_prefix
        )

    def create_operation(self, template: OperationDB) -> int:
        return self._create_template(
            self._template_rep.create_operation, template, _operation_prefix
        )

    def create_rule(self, template: RuleDB) -> int:
        return self._create_template(
            self._template_rep.create_rule, template, _rule_prefix
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

    def _update_template(
        self,
        template: IrregularEventDB | OperationDB | RuleDB,
        get_func,
        update_func,
        node_prefix: str,
    ) -> int:
        self._check_template_rights(
            template.meta.id, template.meta.model_id
        )
        original_template = get_func(template.meta.id)
        obj_id = update_func(template)

        with handle_rollback(update_func, original_template):
            self._visio_service.update_node(
                obj_id, node_prefix, template.meta.name
            )

        return obj_id

    def update_irregular_event(self, template: IrregularEventDB) -> int:
        return self._update_template(
            template,
            self._template_rep.get_irregular_event,
            self._template_rep.update_irregular_event,
            _irregular_event_prefix,
        )

    def update_operation(self, template: OperationDB) -> int:
        return self._update_template(
            template,
            self._template_rep.get_operation,
            self._template_rep.update_operation,
            _operation_prefix,
        )

    def update_rule(self, template: RuleDB) -> int:
        return self._update_template(
            template,
            self._template_rep.get_rule,
            self._template_rep.update_rule,
            _rule_prefix,
        )

    def get_templates(self, model_id: int) -> Templates:
        return Templates(
            irregular_events=self._template_rep.get_irregular_events(model_id),
            operations=self._template_rep.get_operations(model_id),
            rules=self._template_rep.get_rules(model_id),
        )

    def delete_template(self, template_id: int, model_id: int) -> int:
        _get_funcs: Dict[
            str, Callable[[int], Union[IrregularEventDB, OperationDB, RuleDB]]
        ] = {
            "irregular_event": self._template_rep.get_irregular_event,
            "operation": self._template_rep.get_operation,
            "rule": self._template_rep.get_rule,
        }

        _create_funcs: Dict[str, Callable[[Any], int]] = {
            "irregular_event": self._template_rep.create_irregular_event,
            "operation": self._template_rep.create_operation,
            "rule": self._template_rep.create_rule,
        }

        self._check_template_rights(template_id, model_id)
        template_meta = self._template_rep.get_template_meta(template_id)

        get_func = _get_funcs.get(template_meta.type)
        create_func = _create_funcs.get(template_meta.type)
        node_prefix = self._node_prefixes.get(template_meta.type)

        template = get_func(template_meta.id)  # type: ignore
        obj_id = self._template_rep.delete_template(template_meta.id)

        with handle_rollback(create_func, template):
            self._visio_service.delete_node(obj_id, node_prefix)  # type: ignore

        return obj_id

    def create_template_usage(self, template_usage: TemplateUsageDB) -> int:
        obj_id = self._template_rep.create_template_usage(template_usage)

        with handle_rollback(self._template_rep.delete_template_usage, obj_id):
            usage_node_id = self._visio_service.create_node(
                obj_id,
                _template_usage_prefix,
                template_usage.name,
                template_usage.model_id,
            )

        template_meta = self._template_rep.get_template_meta(template_usage.template_id)
        template_prefix = self._node_prefixes.get(template_meta.type)
        template_node_id = self._visio_service.get_node_id(
            template_usage.template_id, template_prefix  # type: ignore
        )

        with handle_rollback(self._visio_service.delete_node, obj_id, usage_node_id):
            with handle_rollback(self._template_rep.delete_template_usage, obj_id):
                self._visio_service.create_edge(
                    template_node_id, usage_node_id, template_usage.model_id
                )

        for argument in template_usage.arguments:
            with handle_rollback(self._template_rep.delete_template_usage, obj_id):
                resource_node_id = self._visio_service.get_node_id(
                    argument.resource_id, _resource_prefix
                )
                self._visio_service.create_edge(
                    usage_node_id, resource_node_id, template_usage.model_id
                )
                
        return obj_id

    def get_template_usage(
        self, template_usage_id: int, model_id: int
    ) -> TemplateUsageDB:
        self._check_template_usage_rights(template_usage_id, model_id)
        return self._template_rep.get_template_usage(template_usage_id)

    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]:
        return self.get_template_usages(model_id)

    def update_template_usage(self, template_usage: TemplateUsageDB) -> int:
        self._check_template_usage_rights(template_usage.id, template_usage.model_id)
        original_template_usage = self._template_rep.get_template_usage(
            template_usage.id
        )
        obj_id = self._template_rep.update_template_usage(template_usage)

        with handle_rollback(
            self._template_rep.update_template_usage, original_template_usage
        ):
            self._visio_service.update_node(
                obj_id, _template_usage_prefix, template_usage.name
            )

        return obj_id

    def delete_template_usage(self, template_usage_id: int, model_id: int) -> int:
        self._check_template_usage_rights(template_usage_id, model_id)
        template_usage = self._template_rep.get_template_usage(template_usage_id)
        obj_id = self._template_rep.delete_template_usage(template_usage_id)

        with handle_rollback(self._template_rep.create_template_usage, template_usage):
            self._visio_service.delete_node(obj_id, _template_usage_prefix)

        return obj_id
