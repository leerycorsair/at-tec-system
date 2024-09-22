from typing import List
from fastapi import APIRouter

from src.service.editor.template.models.models import (
    IrregularEventTemplate,
    OperationTemplate,
    RuleTemplate,
)


router = APIRouter(
    prefix="/templates",
    tags=["editor:templates"],
)


@router.post("/irregular_event", response_model=int)
async def create_irregular_event(body: IrregularEventTemplate):
    pass


@router.post("/operation", response_model=int)
async def create_operation(body: OperationTemplate):
    pass


@router.post("/rule", response_model=int)
async def create_rule(body: RuleTemplate):
    pass


@router.put("/{template_id}/irregular_event", response_model=int)
async def update_irregular_event(body: IrregularEventTemplate):
    pass


@router.put("/{template_id}/operation", response_model=int)
async def update_operation(body: OperationTemplate):
    pass


@router.put("/{template_id}/rule", response_model=int)
async def update_rule(body: RuleTemplate):
    pass


@router.delete("/{template_id}", response_model=int)
async def delete_template():
    pass
