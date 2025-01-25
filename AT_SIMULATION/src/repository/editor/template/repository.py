from typing import Any, Callable, List, Optional, Tuple, TypeVar

from sqlalchemy.orm import Session

from src.repository.editor.template.models.conversions import (
    to_IrregularEventBody, to_IrregularEventDB, to_IrregularEventGenerator,
    to_OperationBody, to_OperationDB, to_RelevantResource, to_RuleBody,
    to_RuleDB, to_Template, to_TemplateMetaDB, to_TemplateUsage,
    to_TemplateUsageArgument, to_TemplateUsageDB)
from src.repository.editor.template.models.models import (IrregularEventDB,
                                                          OperationDB,
                                                          RelevantResourceDB,
                                                          RuleDB,
                                                          TemplateMetaDB,
                                                          TemplateUsageDB)
from src.repository.helper import handle_sqlalchemy_errors
from src.schema.template import (IrregularEventBody, IrregularEventGenerator,
                                 OperationBody, RelevantResource, RuleBody,
                                 Template, TemplateTypeEnum, TemplateUsage,
                                 TemplateUsageArgument)

T = TypeVar("T", IrregularEventDB, OperationDB, RuleDB)


class TemplateRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_irregular_event(self, template: IrregularEventDB) -> int:
        return self._create_template(
            template,
            to_IrregularEventBody,
            to_IrregularEventGenerator,
        )

    @handle_sqlalchemy_errors
    def create_operation(self, template: OperationDB) -> int:
        return self._create_template(template, to_OperationBody)

    @handle_sqlalchemy_errors
    def create_rule(self, template: RuleDB) -> int:
        return self._create_template(template, to_RuleBody)

    @handle_sqlalchemy_errors
    def get_irregular_event(self, template_id: int) -> IrregularEventDB:
        return self._get_template(
            template_id,
            IrregularEventBody,
            to_IrregularEventDB,
            IrregularEventGenerator,
        )

    @handle_sqlalchemy_errors
    def get_operation(self, template_id: int) -> OperationDB:
        return self._get_template(template_id, OperationBody, to_OperationDB)

    @handle_sqlalchemy_errors
    def get_rule(self, template_id: int) -> RuleDB:
        return self._get_template(template_id, RuleBody, to_RuleDB)

    @handle_sqlalchemy_errors
    def update_irregular_event(self, template: IrregularEventDB) -> int:
        return self._update_template(
            template, to_IrregularEventBody, to_IrregularEventGenerator
        )

    @handle_sqlalchemy_errors
    def update_operation(self, template: OperationDB) -> int:
        return self._update_template(template, to_OperationBody)

    @handle_sqlalchemy_errors
    def update_rule(self, template: RuleDB) -> int:
        return self._update_template(template, to_RuleBody)

    @handle_sqlalchemy_errors
    def get_irregular_events(self, model_id: int) -> List[IrregularEventDB]:
        return self._get_templates(
            model_id, self.get_irregular_event, "IRREGULAR_EVENT"
        )

    @handle_sqlalchemy_errors
    def get_operations(self, model_id: int) -> List[OperationDB]:
        return self._get_templates(model_id, self.get_operation, "OPERATION")

    @handle_sqlalchemy_errors
    def get_rules(self, model_id: int) -> List[RuleDB]:
        return self._get_templates(model_id, self.get_rule, "RULE")

    @handle_sqlalchemy_errors
    def get_template_meta(self, template_id: int) -> TemplateMetaDB:
        template_meta, rel_resources = self._get_meta(template_id)
        return to_TemplateMetaDB(template_meta, rel_resources)

    @handle_sqlalchemy_errors
    def delete_template(self, template_id: int) -> int:
        template_meta = (
            self.db_session.query(Template)
            .filter(Template.id == template_id)
            .first()
        )
        if not template_meta:
            raise RuntimeError("Template does not exist")

        self.db_session.delete(template_meta)
        return template_id

    @handle_sqlalchemy_errors
    def create_template_usage(self, template_usage: TemplateUsageDB) -> int:
        new_template_usage = to_TemplateUsage(template_usage)
        self.db_session.add(new_template_usage)
        self.db_session.flush()
        self._process_arguments(template_usage, new_template_usage.id)
        return new_template_usage.id

    @handle_sqlalchemy_errors
    def get_template_usage(self, template_usage_id: int) -> TemplateUsageDB:
        template_usage = self._get_template_usage_by_id(template_usage_id)
        arguments = self._get_arguments_by_usage_id(template_usage.id)
        return to_TemplateUsageDB(template_usage, arguments)

    @handle_sqlalchemy_errors
    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]:
        template_usages = (
            self.db_session.query(TemplateUsage)
            .filter(TemplateUsage.model_id == model_id)
            .all()
        )

        template_usages_db = []
        for usage in template_usages:
            arguments = (
                self.db_session.query(TemplateUsageArgument)
                .filter(TemplateUsageArgument.template_usage_id == usage.id)
                .all()
            )
            template_usages_db.append(to_TemplateUsageDB(usage, arguments))

        return template_usages_db

    @handle_sqlalchemy_errors
    def update_template_usage(self, template_usage: TemplateUsageDB) -> int:
        existing_template_usage = self._get_template_usage_by_id(template_usage.id)
        existing_template_usage.name = template_usage.name
        self._process_arguments(template_usage, existing_template_usage.id)
        return template_usage.id

    @handle_sqlalchemy_errors
    def delete_template_usage(self, template_usage_id: int) -> int:
        template_usage = self._get_template_usage_by_id(template_usage_id)
        self.db_session.delete(template_usage)
        return template_usage_id

    def _get_template_usage_by_id(self, template_usage_id: int) -> TemplateUsage:
        template_usage = (
            self.db_session.query(TemplateUsage).filter_by(id=template_usage_id).first()
        )
        if not template_usage:
            raise RuntimeError("Template usage not found")
        return template_usage

    def _get_arguments_by_usage_id(
        self, template_usage_id: int
    ) -> List[TemplateUsageArgument]:
        return (
            self.db_session.query(TemplateUsageArgument)
            .filter_by(template_usage_id=template_usage_id)
            .all()
        )

    def _process_arguments(
        self, template_usage: TemplateUsageDB, usage_id: int
    ) -> None:
        for arg in template_usage.arguments:
            existing_arg = (
                self.db_session.query(TemplateUsageArgument)
                .filter_by(id=arg.id)
                .first()
            )
            if existing_arg:
                existing_arg.relevant_resource_id = arg.relevant_resource_id
                existing_arg.resource_id = arg.resource_id
            else:
                new_arg = to_TemplateUsageArgument(arg, usage_id)
                self.db_session.add(new_arg)

    def _get_templates(
        self, model_id: int, get_func: Callable[[int], T], template_type: str
    ) -> List[T]:
        template_ids = self._get_template_ids(model_id, template_type)

        results = []
        for template_id in template_ids:
            results.append(get_func(template_id))

        return results

    def _create_template_meta(self, meta: TemplateMetaDB) -> Template:
        new_template = to_Template(meta)
        self.db_session.add(new_template)
        self.db_session.flush()
        self._create_relevant_resources(new_template.id, meta.rel_resources)

        return new_template

    def _create_relevant_resources(
        self, template_id: int, rel_resources: List[RelevantResourceDB]
    ) -> None:
        relevant_resources = [
            to_RelevantResource(res, template_id) for res in rel_resources
        ]
        self.db_session.add_all(relevant_resources)

    def _get_meta(self, template_id: int) -> Tuple[Template, List[RelevantResource]]:
        template_meta = (
            self.db_session.query(Template).filter(Template.id == template_id).first()
        )
        if not template_meta:
            raise RuntimeError("Template does not exist")

        rel_resources = (
            self.db_session.query(RelevantResource)
            .filter(RelevantResource.template_id == template_id)
            .all()
        )

        return template_meta, rel_resources

    def _update_relevant_resources(
        self, template_id: int, rel_resources: List[RelevantResourceDB]
    ) -> None:
        self._delete_template_relevant_resources(template_id)
        self._create_relevant_resources(template_id, rel_resources)

    def _delete_template_relevant_resources(self, template_id: int) -> None:
        (
            self.db_session.query(RelevantResource)
            .filter(RelevantResource.template_id == template_id)
            .delete(synchronize_session=False)
        )

    def _update_meta(self, meta: TemplateMetaDB) -> Template:
        update_meta, _ = self._get_meta(meta.id)
        self._delete_template_parts(update_meta.id, TemplateTypeEnum(update_meta.type))

        update_meta.name = meta.name
        update_meta.type = meta.type

        self._update_relevant_resources(meta.id, meta.rel_resources)

        return update_meta

    def _delete_template_parts(
        self, template_id: int, template_type: TemplateTypeEnum
    ) -> None:
        match template_type:
            case TemplateTypeEnum.IRREGULAR_EVENT:
                self._delete_template_part(template_id, IrregularEventBody)
                self._delete_template_part(template_id, IrregularEventGenerator)
            case TemplateTypeEnum.OPERATION:
                self._delete_template_part(template_id, OperationBody)
            case TemplateTypeEnum.RULE:
                self._delete_template_part(template_id, RuleBody)

    def _delete_template_part(self, template_id: int, part_table: Any) -> None:
        (
            self.db_session.query(part_table)
            .filter(part_table.template_id == template_id)
            .delete(synchronize_session=False)
        )

    def _get_template_ids(self, model_id: int, template_type: str) -> List[int]:
        return [
            template_id
            for template_id, in (
                self.db_session.query(Template.id)
                .filter(Template.model_id == model_id, Template.type == template_type)
                .all()
            )
        ]

    def _get_template_part(self, template_id: int, part_table: Any) -> Any:
        part = (
            self.db_session.query(part_table)
            .filter(part_table.template_id == template_id)
            .first()
        )
        if not part:
            raise RuntimeError(f"{part_table.__name__} does not exist")
        return part

    def _update_template(
        self,
        template: T,
        body_func: Callable[[Any, int], Any],
        generator_func: Optional[Callable[[Any, int], Any]] = None,
    ) -> int:
        template_meta = self._update_meta(template.meta)

        if generator_func:
            new_generator = generator_func(template.generator, template_meta.id)
            self.db_session.add(new_generator)

        new_body = body_func(template.body, template_meta.id)
        self.db_session.add(new_body)

        return template_meta.id

    def _create_template(
        self,
        template: T,
        body_func: Callable[[Any, int], Any],
        generator_func: Optional[Callable[[Any, int], Any]] = None,
    ) -> int:
        new_template = self._create_template_meta(template.meta)

        if generator_func:
            new_generator = generator_func(template.generator, new_template.id)
            self.db_session.add(new_generator)

        new_body = body_func(template.body, new_template.id)
        self.db_session.add(new_body)

        return new_template.id

    def _get_template(
        self,
        template_id: int,
        body_class: Any,
        conversion_func: Callable,
        generator_class: Any = None,
    ) -> T:
        template_meta, rel_resources = self._get_meta(template_id)
        body = self._get_template_part(template_id, body_class)

        generator = None
        if generator_class:
            generator = self._get_template_part(template_id, generator_class)
            return conversion_func(template_meta, rel_resources, body, generator)

        return conversion_func(template_meta, rel_resources, body)
