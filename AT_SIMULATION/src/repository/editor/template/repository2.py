from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.repository.editor.template.conversions import (
    to_TemplateUsage,
    to_TemplateUsageArgument,
    to_TemplateUsageDB,
)
from src.repository.editor.template.models.models import (
    TemplateUsageDB,
)
from src.store.postgres.session import get_db
from src.schema.template import (
    TemplateUsage,
    TemplateUsageArgument,
)


class TemplateRepository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db_session = db_session

    def create_template_usage(self, template_usage: TemplateUsageDB) -> int:
        try:
            new_template_usage = to_TemplateUsage(template_usage)

            self.db_session.add(new_template_usage)
            self.db_session.commit()
            self.db_session.refresh(new_template_usage)

            new_usage_arguments = [
                to_TemplateUsageArgument(arg, new_template_usage.id)
                for arg in template_usage.arguments
            ]

            self.db_session.add_all(new_usage_arguments)
            self.db_session.commit()
            return new_template_usage.id

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to create template usage: {e}") from e

    def get_template_usage(self, template_usage_id: int) -> TemplateUsageDB:
        try:
            template_usage = (
                self.db_session.query(TemplateUsage)
                .filter(TemplateUsage.id == template_usage_id)
                .first()
            )
            if not template_usage:
                raise RuntimeError("Template usage does not exist")

            arguments = (
                self.db_session.query(TemplateUsageArgument)
                .filter(TemplateUsageArgument.template_usage_id == template_usage.id)
                .all()
            )
            return to_TemplateUsageDB(template_usage, arguments)

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get template usage: {e}") from e

    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]:
        try:
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

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get template usages: {e}") from e

    def update_template_usage(self, template_usage: TemplateUsageDB) -> TemplateUsageDB:
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
                    self.db_session.query(TemplateUsageArgument)
                    .filter(TemplateUsageArgument.id == arg.id)
                    .first()
                )

                if existing_arg:
                    existing_arg.relevant_resource_id = arg.relevant_resource_id
                    existing_arg.resource_id = arg.resource_id
                else:
                    new_arg = to_TemplateUsageArgument(arg, existing_template_usage.id)
                    self.db_session.add(new_arg)

            self.db_session.commit()

            return template_usage

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to update template usage: {e}") from e

    def delete_template_usage(self, template_usage_id: int) -> None:
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
            raise RuntimeError(f"Failed to delete template usage: {e}") from e
