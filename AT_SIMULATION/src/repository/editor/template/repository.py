from typing import List, Optional, Type, Union
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.repository.editor.template.models.models import (
    IrregularEventBodyDB,
    IrregularEventGeneratorDB,
    IrregularEventTemplateDB,
    OperationBodyDB,
    OperationTemplateDB,
    RelevantResourceDB,
    RuleBodyDB,
    RuleTemplateDB,
    TemplateMetaDB,
    TemplateUsageDB,
    TemplateUsageArgumentDB,
    TemplateTypeEnum,
)
from src.store.postgres.session import get_db
from src.schema.template import (
    Template,
    RelevantResource,
    TemplateUsage,
    IrregularEventBody,
    IrregularEventGenerator,
    OperationBodies,
    RuleBodies,
)


class TemplateRepository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db_session = db_session

    async def create_template(
        self,
        template_data: Union[
            IrregularEventTemplateDB, OperationTemplateDB, RuleTemplateDB
        ],
        body_model: Type[Union[IrregularEventBody, OperationBodies, RuleBodies]],
        generator_model: Optional[Type[IrregularEventGenerator]] = None,
    ) -> int:
        try:
            new_template = Template(
                name=template_data.template_meta.name,
                type=template_data.template_meta.type,
                model_id=template_data.template_meta.model_id,
            )

            self.db_session.add(new_template)
            self.db_session.commit()
            self.db_session.refresh(new_template)

            if generator_model:
                new_generator = generator_model(
                    type=template_data.generator.type,
                    value=template_data.generator.value,
                    dispersion=template_data.generator.dispersion,
                    template_id=new_template.id,
                )
                self.db_session.add(new_generator)

            new_body = body_model(
                condition=(
                    template_data.body.condition
                    if hasattr(template_data.body, "condition")
                    else None
                ),
                body_before=(
                    template_data.body.body_before
                    if hasattr(template_data.body, "body_before")
                    else None
                ),
                delay=(
                    template_data.body.delay
                    if hasattr(template_data.body, "delay")
                    else None
                ),
                body=template_data.body.body,
                body_after=(
                    template_data.body.body_after
                    if hasattr(template_data.body, "body_after")
                    else None
                ),
                template_id=new_template.id,
            )

            self.db_session.add(new_body)
            self.db_session.commit()
            return new_template.id

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to create template: {e}")

    async def get_template(
        self,
        template_id: int,
        body_model: Type[Union[IrregularEventBody, OperationBodies, RuleBodies]],
        generator_model: Optional[Type[IrregularEventGenerator]] = None,
    ) -> Optional[Union[IrregularEventTemplateDB, OperationTemplateDB, RuleTemplateDB]]:
        try:
            template = self._get_template_base(template_id)
            if not template:
                return None

            body = self._get_body(template_id, body_model)
            generator = (
                self._get_generator(template_id, generator_model)
                if generator_model
                else None
            )
            relevant_resources = self._get_relevant_resources(template_id)

            return self._construct_template_db(
                template, body, generator, relevant_resources
            )

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get template: {e}")

    async def get_irregular_event_templates(self) -> List[IrregularEventTemplateDB]:
        try:
            templates = (
                self.db_session.query(Template)
                .filter(Template.type == TemplateTypeEnum.IRREGULAR_EVENT)
                .all()
            )

            result = []
            for template in templates:
                body = self._get_body(template.id, IrregularEventBody)
                generator = self._get_generator(template.id, IrregularEventGenerator)
                relevant_resources = self._get_relevant_resources(template.id)
                result.append(
                    self._construct_template_db(
                        template, body, generator, relevant_resources
                    )
                )

            return result

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get irregular event templates: {e}")

    async def get_operation_templates(self) -> List[OperationTemplateDB]:
        try:
            templates = (
                self.db_session.query(Template)
                .filter(Template.type == TemplateTypeEnum.OPERATION)
                .all()
            )

            result = []
            for template in templates:
                body = self._get_body(template.id, OperationBodies)
                relevant_resources = self._get_relevant_resources(template.id)
                result.append(
                    self._construct_template_db(
                        template, body, None, relevant_resources
                    )
                )

            return result

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get operation templates: {e}")

    async def get_rule_templates(self) -> List[RuleTemplateDB]:
        try:
            templates = (
                self.db_session.query(Template)
                .filter(Template.type == TemplateTypeEnum.RULE)
                .all()
            )

            result = []
            for template in templates:
                body = self._get_body(template.id, RuleBodies)
                relevant_resources = self._get_relevant_resources(template.id)
                result.append(
                    self._construct_template_db(
                        template, body, None, relevant_resources
                    )
                )

            return result

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get rule templates: {e}")

    async def update_template(
        self,
        template_data: Union[
            IrregularEventTemplateDB, OperationTemplateDB, RuleTemplateDB
        ],
        body_model: Type[Union[IrregularEventBody, OperationBodies, RuleBodies]],
        generator_model: Optional[Type[IrregularEventGenerator]] = None,
    ) -> int:
        try:
            template = self._get_template_base(template_data.template_meta.id)
            if not template:
                raise RuntimeError(f"Template not found")

            template.name = template_data.template_meta.name
            self.db_session.commit()

            body = self._get_body(template.id, body_model)
            if generator_model:
                generator = self._get_generator(template.id, generator_model)
                generator.type = template_data.generator.type
                generator.value = template_data.generator.value
                generator.dispersion = template_data.generator.dispersion

            body.condition = (
                template_data.body.condition
                if hasattr(template_data.body, "condition")
                else None
            )
            body.body_before = (
                template_data.body.body_before
                if hasattr(template_data.body, "body_before")
                else None
            )
            body.delay = (
                template_data.body.delay
                if hasattr(template_data.body, "delay")
                else None
            )
            body.body = template_data.body.body
            body.body_after = (
                template_data.body.body_after
                if hasattr(template_data.body, "body_after")
                else None
            )

            self.db_session.commit()
            return template.id

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to update template: {e}")

    async def delete_template(self, template_id: int) -> None:
        try:
            template = self._get_template_base(template_id)
            if not template:
                raise RuntimeError("Template not found")

            self.db_session.delete(template)
            self.db_session.commit()

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to delete template: {e}")

    async def create_template_usage(self, template_usage: TemplateUsageDB) -> int:
        try:
            new_template_usage = TemplateUsage(
                name=template_usage.name,
                template_id=template_usage.template_id,
                model_id=template_usage.model_id,
            )

            self.db_session.add(new_template_usage)
            self.db_session.commit()
            self.db_session.refresh(new_template_usage)

            new_usage_arguments = [
                TemplateUsageArgumentDB(
                    relevant_resource_id=arg.relevant_resource_id,
                    template_usage_id=new_template_usage.id,
                    resource_id=arg.resource_id,
                )
                for arg in template_usage.arguments
            ]

            self.db_session.add_all(new_usage_arguments)
            self.db_session.commit()
            return new_template_usage.id

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to create template usage: {e}")

    async def get_template_usage(
        self, template_usage_id: int
    ) -> Optional[TemplateUsageDB]:
        try:
            template_usage = (
                self.db_session.query(TemplateUsage)
                .filter(TemplateUsage.id == template_usage_id)
                .first()
            )
            if not template_usage:
                return None

            arguments = (
                self.db_session.query(TemplateUsageArgumentDB)
                .filter(TemplateUsageArgumentDB.template_usage_id == template_usage.id)
                .all()
            )

            return TemplateUsageDB(
                id=template_usage.id,
                name=template_usage.name,
                template_id=template_usage.template_id,
                model_id=template_usage.model_id,
                arguments=arguments,
            )

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get template usage: {e}")

    async def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]:
        try:
            template_usages = (
                self.db_session.query(TemplateUsage)
                .filter(TemplateUsage.model_id == model_id)
                .all()
            )

            template_usages_db = []
            for usage in template_usages:
                arguments = (
                    self.db_session.query(TemplateUsageArgumentDB)
                    .filter(TemplateUsageArgumentDB.template_usage_id == usage.id)
                    .all()
                )

                template_usages_db.append(
                    TemplateUsageDB(
                        id=usage.id,
                        name=usage.name,
                        template_id=usage.template_id,
                        model_id=usage.model_id,
                        arguments=arguments,
                    )
                )

            return template_usages_db

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get template usages: {e}")

    async def update_template_usage(
        self, template_usage: TemplateUsageDB
    ) -> TemplateUsageDB:
        try:
            existing_template_usage = (
                self.db_session.query(TemplateUsage)
                .filter(TemplateUsage.id == template_usage.id)
                .first()
            )
            if not existing_template_usage:
                raise RuntimeError("Template usage not found")

            existing_template_usage.name = template_usage.name
            self.db_session.commit()

            for arg in template_usage.arguments:
                existing_arg = (
                    self.db_session.query(TemplateUsageArgumentDB)
                    .filter(TemplateUsageArgumentDB.id == arg.id)
                    .first()
                )

                if existing_arg:
                    existing_arg.relevant_resource_id = arg.relevant_resource_id
                    existing_arg.resource_id = arg.resource_id
                else:
                    new_arg = TemplateUsageArgumentDB(
                        relevant_resource_id=arg.relevant_resource_id,
                        template_usage_id=existing_template_usage.id,
                        resource_id=arg.resource_id,
                    )
                    self.db_session.add(new_arg)

            self.db_session.commit()

            return template_usage

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to update template usage: {e}")

    async def delete_template_usage(self, template_usage_id: int) -> None:
        try:
            template_usage = (
                self.db_session.query(TemplateUsage)
                .filter(TemplateUsage.id == template_usage_id)
                .first()
            )
            if not template_usage:
                raise RuntimeError("Template usage not found")

            self.db_session.delete(template_usage)
            self.db_session.commit()

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to delete template usage: {e}")

    def _get_template_base(self, template_id: int) -> Optional[Template]:
        return (
            self.db_session.query(Template).filter(Template.id == template_id).first()
        )

    def _get_body(
        self,
        template_id: int,
        body_model: Type[Union[IrregularEventBody, OperationBodies, RuleBodies]],
    ) -> Optional[Union[IrregularEventBody, OperationBodies, RuleBodies]]:
        return (
            self.db_session.query(body_model)
            .filter(body_model.template_id == template_id)
            .first()
        )

    def _get_generator(
        self, template_id: int, generator_model: Type[IrregularEventGenerator]
    ) -> Optional[IrregularEventGenerator]:
        return (
            self.db_session.query(generator_model)
            .filter(generator_model.template_id == template_id)
            .first()
        )

    def _get_relevant_resources(self, template_id: int) -> List[RelevantResource]:
        return (
            self.db_session.query(RelevantResource)
            .filter(RelevantResource.template_id == template_id)
            .all()
        )

    def _construct_template_db(
        self,
        template: Template,
        body: Union[IrregularEventBody, OperationBodies, RuleBodies],
        generator: Optional[IrregularEventGenerator],
        relevant_resources: List[RelevantResource],
    ) -> Union[IrregularEventTemplateDB, OperationTemplateDB, RuleTemplateDB]:
        return {
            TemplateTypeEnum.IRREGULAR_EVENT: IrregularEventTemplateDB(
                template_meta=self._construct_template_meta(
                    template, relevant_resources
                ),
                generator=(
                    self._construct_generator_db(generator) if generator else None
                ),
                body=self._construct_body_db(body),
            ),
            TemplateTypeEnum.OPERATION: OperationTemplateDB(
                template_meta=self._construct_template_meta(
                    template, relevant_resources
                ),
                body=self._construct_body_db(body),
            ),
            TemplateTypeEnum.RULE: RuleTemplateDB(
                template_meta=self._construct_template_meta(
                    template, relevant_resources
                ),
                body=self._construct_body_db(body),
            ),
        }[template.type]

    def _construct_template_meta(
        self, template: Template, relevant_resources: List[RelevantResource]
    ) -> TemplateMetaDB:
        return TemplateMetaDB(
            id=template.id,
            name=template.name,
            type=template.type,
            rel_resources=[
                RelevantResourceDB(
                    id=res.id,
                    name=res.name,
                    template_id=res.template_id,
                    resource_type_id=res.resource_type_id,
                )
                for res in relevant_resources
            ],
        )

    def _construct_generator_db(
        self, generator: IrregularEventGenerator
    ) -> IrregularEventGeneratorDB:
        return IrregularEventGeneratorDB(
            id=generator.id,
            type=generator.type,
            value=generator.value,
            dispersion=generator.dispersion,
            template_id=generator.template_id,
        )

    def _construct_body_db(
        self, body: Union[IrregularEventBody, OperationBodies, RuleBodies]
    ) -> Union[IrregularEventBodyDB, OperationBodyDB, RuleBodyDB]:
        if isinstance(body, IrregularEventBody):
            return IrregularEventBodyDB(
                id=body.id,
                body=body.body,
                template_id=body.template_id,
            )
        elif isinstance(body, OperationBodies):
            return OperationBodyDB(
                id=body.id,
                condition=body.condition,
                body_before=body.body_before,
                delay=body.delay,
                body_after=body.body_after,
                template_id=body.template_id,
            )
        elif isinstance(body, RuleBodies):
            return RuleBodyDB(
                id=body.id,
                condition=body.condition,
                body=body.body,
                template_id=body.template_id,
            )
