from typing import List
from src.repository.editor.template.models.models import (
    TemplateUsageArgumentDB,
    TemplateUsageDB,
)
from src.schema.template import TemplateUsage, TemplateUsageArgument


def to_TemplateUsage(template_usage: TemplateUsageDB) -> TemplateUsage:
    return TemplateUsage(
        name=template_usage.name,
        template_id=template_usage.template_id,
        model_id=template_usage.model_id,
    )


def to_TemplateUsageArgument(
    arg: TemplateUsageArgumentDB, template_usage_id: int
) -> TemplateUsageArgument:
    return TemplateUsageArgument(
        relevant_resource_id=arg.relevant_resource_id,
        template_usage_id=template_usage_id,
        resource_id=arg.resource_id,
    )


def to_TemplateUsageArgumentDB(arg: TemplateUsageArgument) -> TemplateUsageArgumentDB:
    return TemplateUsageArgumentDB(
        id=arg.id,
        relevant_resource_id=arg.relevant_resource_id,
        template_usage_id=arg.template_usage_id,
        resource_id=arg.resource_id,
    )


def to_TemplateUsageDB(
    template_usage: TemplateUsage, args: List[TemplateUsageArgument]
) -> TemplateUsageDB:
    return TemplateUsageDB(
        id=template_usage.id,
        name=template_usage.name,
        template_id=template_usage.template_id,
        arguments=[to_TemplateUsageArgumentDB(arg) for arg in args],
        model_id=template_usage.model_id,
    )
