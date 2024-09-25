from fastapi import APIRouter, Depends

from src.delivery.core.models.conversions import to_ObjectIDResponse
from src.delivery.core.models.models import ObjectIDResponse
from src.delivery.editor.template.dependencies import (
    ITemplateService,
    get_template_service,
)


from src.delivery.editor.template.models.conversions import (
    to_IrregularEventDB,
    to_IrregularEventResponse,
    to_OperationDB,
    to_OperationResponse,
    to_RuleDB,
    to_RuleResponse,
    to_TemplateUsageDB,
    to_TemplateUsageResponse,
    to_TemplateUsagesResponse,
    to_TemplatesResponse,
)
from src.delivery.editor.template.models.models import (
    IrregularEventRequest,
    IrregularEventResponse,
    OperationRequest,
    OperationResponse,
    RuleRequest,
    RuleResponse,
    TemplateUsageRequest,
    TemplateUsageResponse,
    TemplateUsagesResponse,
    TemplatesResponse,
)
from src.delivery.model.dependencies import get_current_model

router = APIRouter(
    prefix="/templates",
    tags=["editor:templates"],
)


@router.post("/irregular_event", response_model=ObjectIDResponse)
async def create_irregular_event(
    body: IrregularEventRequest,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.create_irregular_event(
            to_IrregularEventDB(body, model_id),
        )
    )


@router.post("/operation", response_model=ObjectIDResponse)
async def create_operation(
    body: OperationRequest,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.create_operation(
            to_OperationDB(body, model_id),
        )
    )


@router.post("/rule", response_model=ObjectIDResponse)
async def create_rule(
    body: RuleRequest,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.create_rule(
            to_RuleDB(body, model_id),
        )
    )


@router.get("/", response_model=TemplatesResponse)
async def get_templates(
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> TemplatesResponse:
    return to_TemplatesResponse(await template_service.get_templates(model_id))


@router.get("/{template_id}/irregular_event", response_model=IrregularEventResponse)
async def get_irregular_event(
    template_id: int,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> IrregularEventResponse:
    return to_IrregularEventResponse(
        await template_service.get_irregular_event(template_id, model_id)
    )


@router.get("/{template_id}/operation", response_model=OperationResponse)
async def get_operation(
    template_id: int,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> OperationResponse:
    return to_OperationResponse(
        await template_service.get_operation(template_id, model_id)
    )


@router.get("/{template_id}/rule", response_model=RuleResponse)
async def get_rule(
    template_id: int,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> RuleResponse:
    return to_RuleResponse(
        await template_service.get_rule(template_id, model_id)
    )


@router.put("/{template_id}/irregular_event", response_model=ObjectIDResponse)
async def update_irregular_event(
    body: IrregularEventRequest,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.update_irregular_event(
            to_IrregularEventDB(body, model_id)
        )
    )


@router.put("/{template_id}/operation", response_model=ObjectIDResponse)
async def update_operation(
    body: OperationRequest,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.update_operation(to_OperationDB(body, model_id))
    )


@router.put("/{template_id}/rule", response_model=ObjectIDResponse)
async def update_rule(
    body: RuleRequest,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.update_rule(to_RuleDB(body, model_id))
    )


@router.delete("/{template_id}", response_model=ObjectIDResponse)
async def delete_template(
    template_id: int,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.delete_template(template_id, model_id)
    )


@router.post("/usages", response_model=ObjectIDResponse)
async def create_usage(
    body: TemplateUsageRequest,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.create_template_usage(to_TemplateUsageDB(body, model_id))
    )


@router.get("/usages", response_model=TemplateUsagesResponse)
async def get_usages(
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> TemplateUsagesResponse:
    return to_TemplateUsagesResponse(await template_service.get_template_usages(model_id))


@router.get("/usages/{usage_id}", response_model=TemplateUsageResponse)
async def get_usage(
    usage_id: int,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> TemplateUsageResponse:
    return to_TemplateUsageResponse(
        await template_service.get_template_usage(usage_id, model_id)
    )


@router.put("/usages/{usage_id}", response_model=ObjectIDResponse)
async def update_usage(
    body: TemplateUsageRequest,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.update_template_usage(to_TemplateUsageDB(body, model_id))
    )


@router.delete("/usages/{usage_id}", response_model=ObjectIDResponse)
async def delete_usage(
    usage_id: int,
    model_id: int = Depends(get_current_model),
    template_service: ITemplateService = Depends(get_template_service),
) -> ObjectIDResponse:
    return to_ObjectIDResponse(
        await template_service.delete_template_usage(usage_id, model_id)
    )
