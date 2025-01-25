from typing import List

from src.repository.editor.template.models.models import (
    IrregularEventBodyDB,
    IrregularEventDB,
    IrregularEventGeneratorDB,
    OperationBodyDB,
    OperationDB,
    RelevantResourceDB,
    RuleBodyDB,
    RuleDB,
    TemplateMetaDB,
    TemplateUsageArgumentDB,
    TemplateUsageDB,
)
from src.schema.template import (
    IrregularEventBody,
    IrregularEventGenerator,
    OperationBody,
    RelevantResource,
    RuleBody,
    Template,
    TemplateUsage,
    TemplateUsageArgument,
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


def to_IrregularEventDB(
    meta: Template,
    rel_resources: List[RelevantResource],
    body: IrregularEventBody,
    generator: IrregularEventGenerator,
) -> IrregularEventDB:
    return IrregularEventDB(
        meta=to_TemplateMetaDB(meta, rel_resources),
        generator=IrregularEventGeneratorDB(
            type=generator.type,
            value=generator.value,
            dispersion=generator.dispersion,
            template_id=generator.template_id,
        ),
        body=IrregularEventBodyDB(
            body=body.body,
            template_id=body.template_id,
        ),
    )


def to_OperationDB(
    meta: Template,
    rel_resources: List[RelevantResource],
    body: OperationBody,
) -> OperationDB:
    return OperationDB(
        meta=to_TemplateMetaDB(meta, rel_resources),
        body=OperationBodyDB(
            condition=body.condition,
            body_before=body.body_before,
            delay=body.delay,
            body_after=body.body_after,
            template_id=body.template_id,
        ),
    )


def to_RuleDB(
    meta: Template,
    rel_resources: List[RelevantResource],
    body: RuleBody,
) -> RuleDB:
    return RuleDB(
        meta=to_TemplateMetaDB(meta, rel_resources),
        body=RuleBodyDB(
            condition=body.condition,
            body=body.body,
            template_id=body.template_id,
        ),
    )


def to_RelevantResourceDB(res: RelevantResource) -> RelevantResourceDB:
    return RelevantResourceDB(
        id=res.id,
        name=res.name,
        template_id=res.template_id,
        resource_type_id=res.resource_type_id,
    )


def to_TemplateMetaDB(
    meta: Template,
    rel_resources: List[RelevantResource],
) -> TemplateMetaDB:
    return TemplateMetaDB(
        id=meta.id,
        name=meta.name,
        type=meta.type,
        rel_resources=[to_RelevantResourceDB(res) for res in rel_resources],
        model_id=meta.model_id,
    )
