from typing import List

from src.delivery.editor.template.models.models import (
    GeneratorTypeEnum, IrregularEventBody, IrregularEventGenerator,
    IrregularEventRequest, IrregularEventResponse, OperationBody,
    OperationRequest, OperationResponse, RelevantResourceRequest,
    RelevantResourceResponse, RuleBody, RuleRequest, RuleResponse,
    TemplateMetaRequest, TemplateMetaResponse, TemplatesResponse,
    TemplateTypeEnum, TemplateUsageArgumentRequest,
    TemplateUsageArgumentResponse, TemplateUsageRequest, TemplateUsageResponse,
    TemplateUsagesResponse)
from src.repository.editor.template.models.models import (
    IrregularEventBodyDB, IrregularEventDB, IrregularEventGeneratorDB,
    OperationBodyDB, OperationDB, RelevantResourceDB, RuleBodyDB, RuleDB,
    TemplateMetaDB, TemplateUsageArgumentDB, TemplateUsageDB)
from src.service.editor.template.models.models import Templates


def to_RelevantResourceDB(
    resource: RelevantResourceRequest,
    template_id: int,
) -> RelevantResourceDB:
    return RelevantResourceDB(
        id=resource.id or 0,
        name=resource.name,
        template_id=template_id,
        resource_type_id=resource.resource_type_id,
    )


def to_TemplateMetaDB(
    meta: TemplateMetaRequest,
    model_id: int,
) -> TemplateMetaDB:
    return TemplateMetaDB(
        id=meta.id or 0,
        name=meta.name,
        type=meta.type.value,
        rel_resources=[
            to_RelevantResourceDB(resource, meta.id or 0)
            for resource in meta.rel_resources
        ],
        model_id=model_id,
    )


def to_IrregularEventDB(
    template: IrregularEventRequest,
    model_id: int,
) -> IrregularEventDB:
    return IrregularEventDB(
        meta=to_TemplateMetaDB(template.meta, model_id),
        generator=IrregularEventGeneratorDB(
            type=template.generator.type.value,
            value=template.generator.value,
            dispersion=template.generator.dispersion,
            template_id=template.meta.id or 0,
        ),
        body=IrregularEventBodyDB(
            body=template.body.body,
            template_id=template.meta.id or 0,
        ),
    )


def to_OperationDB(
    template: OperationRequest,
    model_id: int,
) -> OperationDB:
    return OperationDB(
        meta=to_TemplateMetaDB(template.meta, model_id),
        body=OperationBodyDB(
            condition=template.body.condition,
            body_before=template.body.body_before,
            delay=template.body.delay,
            body_after=template.body.body_after,
            template_id=template.meta.id or 0,
        ),
    )


def to_RuleDB(
    template: RuleRequest,
    model_id: int,
) -> RuleDB:
    return RuleDB(
        meta=to_TemplateMetaDB(template.meta, model_id),
        body=RuleBodyDB(
            condition=template.body.condition,
            body=template.body.body,
            template_id=template.meta.id or 0,
        ),
    )


def to_RelevantResourceRespone(
    resource: RelevantResourceDB,
) -> RelevantResourceResponse:
    return RelevantResourceResponse(
        id=resource.id,
        name=resource.name,
        resource_type_id=resource.resource_type_id,
    )


def to_TemplateMetaResponse(meta: TemplateMetaDB) -> TemplateMetaResponse:
    return TemplateMetaResponse(
        id=meta.id,
        name=meta.name,
        type=TemplateTypeEnum(meta.type),
        rel_resources=[
            to_RelevantResourceRespone(resource) for resource in meta.rel_resources
        ],
    )


def to_TemplatesResponse(templates: Templates) -> TemplatesResponse:
    return TemplatesResponse(
        irregular_events=[
            to_IrregularEventResponse(template)
            for template in templates.irregular_events
        ],
        operations=[
            to_OperationResponse(template) for template in templates.operations
        ],
        rules=[to_RuleResponse(template) for template in templates.rules],
        total=len(templates.rules)
        + len(templates.operations)
        + len(templates.irregular_events),
    )


def to_IrregularEventResponse(template: IrregularEventDB) -> IrregularEventResponse:
    return IrregularEventResponse(
        meta=to_TemplateMetaResponse(template.meta),
        generator=IrregularEventGenerator(
            type=GeneratorTypeEnum(template.generator.type),
            value=template.generator.value,
            dispersion=template.generator.dispersion,
        ),
        body=IrregularEventBody(
            body=template.body.body,
        ),
    )


def to_OperationResponse(template: OperationDB) -> OperationResponse:
    return OperationResponse(
        meta=to_TemplateMetaResponse(template.meta),
        body=OperationBody(
            condition=template.body.condition,
            body_before=template.body.body_before,
            delay=template.body.delay,
            body_after=template.body.body_after,
        ),
    )


def to_RuleResponse(template: RuleDB) -> RuleResponse:
    return RuleResponse(
        meta=to_TemplateMetaResponse(template.meta),
        body=RuleBody(
            condition=template.body.condition,
            body=template.body.body,
        ),
    )


def to_TemplateUsageArgumentDB(
    arg: TemplateUsageArgumentRequest, usage_id: int
) -> TemplateUsageArgumentDB:
    return TemplateUsageArgumentDB(
        id=arg.id or 0,
        relevant_resource_id=arg.relevant_resource_id,
        template_usage_id=usage_id,
        resource_id=arg.resource_id,
    )


def to_TemplateUsageDB(usage: TemplateUsageRequest, model_id: int) -> TemplateUsageDB:
    return TemplateUsageDB(
        id=usage.id or 0,
        name=usage.name,
        template_id=usage.template_id,
        arguments=[
            to_TemplateUsageArgumentDB(arg, usage.id or 0) for arg in usage.arguments
        ],
        model_id=model_id,
    )


def to_TemplateUsageArgumentResponse(
    arg: TemplateUsageArgumentDB,
) -> TemplateUsageArgumentResponse:
    return TemplateUsageArgumentResponse(
        id=arg.id,
        relevant_resource_id=arg.relevant_resource_id,
        resource_id=arg.resource_id,
    )


def to_TemplateUsageResponse(usage: TemplateUsageDB) -> TemplateUsageResponse:
    return TemplateUsageResponse(
        id=usage.id,
        name=usage.name,
        template_id=usage.template_id,
        arguments=[to_TemplateUsageArgumentResponse(arg) for arg in usage.arguments],
    )


def to_TemplateUsagesResponse(usages: List[TemplateUsageDB]) -> TemplateUsagesResponse:
    return TemplateUsagesResponse(
        usages=[to_TemplateUsageResponse(usage) for usage in usages],
        total=len(usages),
    )
