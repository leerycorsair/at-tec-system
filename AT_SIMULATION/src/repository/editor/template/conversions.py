from typing import List
from src.repository.editor.template.models.models import (
    IrregularEventBodyDB,
    IrregularEventGeneratorDB,
    OperationBodyDB,
    RelevantResourceDB,
    RuleBodyDB,
    TemplateMetaDB,
    TemplateUsageArgumentDB,
    TemplateUsageDB,
)
from src.schema.template import (
    IrregularEventBody,
    OperationBody,
    RelevantResource,
    Template,
    RuleBody,
    TemplateUsage,
    TemplateUsageArgument,
    IrregularEventGenerator,
)


def to_Template(meta: TemplateMetaDB) -> Template:
    return Template(
        name=meta.name,
        type=meta.type,
        model_id=meta.model_id,
    )


def to_IrregularEventGenerator(
    gen: IrregularEventGeneratorDB, template_id: int
) -> IrregularEventGenerator:
    return IrregularEventGenerator(
        type=gen.type,
        value=gen.value,
        dispersion=gen.dispersion,
        template_id=template_id,
    )


def to_IrregularEventBody(
    body: IrregularEventBodyDB, template_id: int
) -> IrregularEventBody:
    return IrregularEventBody(
        body=body.body,
        template_id=template_id,
    )


def to_OperationBody(body: OperationBodyDB, template_id: int) -> OperationBody:
    return OperationBody(
        condition=body.condition,
        body_before=body.body_before,
        delay=body.delay,
        body_after=body.body_after,
        template_id=template_id,
    )


def to_RuleBody(body: RuleBodyDB, template_id: int) -> RuleBody:
    return RuleBody(
        condition=body.condition,
        body=body.body,
        template_id=template_id,
    )


def to_RelevantResource(res: RelevantResourceDB, template_id: int) -> RelevantResource:
    return RelevantResource(
        name=res.name,
        template_id=template_id,
        resource_type_id=res.resource_type_id,
    )


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


def to_IrregularEventDB():
    pass


def to_OperationDB():
    pass


def to_RuleDB():
    pass


def to_TemplateMetaDB():
    pass
