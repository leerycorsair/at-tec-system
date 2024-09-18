from typing import List
from fastapi import APIRouter

from src.dto.api.editor.template import (
    IrregularEventTemplate,
    OperationTemplate,
    RuleTemplate,
)


template_router = APIRouter(
    prefix="/templates",
    tags=["editor:templates"],
)


@template_router.post("/irregular_event", response_model=int)
async def create_irregular_event(body: IrregularEventTemplate):
    pass


@template_router.post("/operation", response_model=int)
async def create_operation(body: OperationTemplate):
    pass


@template_router.post("/rule", response_model=int)
async def create_rule(body: RuleTemplate):
    pass


@template_router.put("/{template_id}/irregular_event", response_model=int)
async def update_irregular_event(body: IrregularEventTemplate):
    pass


@template_router.put("/{template_id}/operation", response_model=int)
async def update_operation(body: OperationTemplate):
    pass


@template_router.put("/{template_id}/rule", response_model=int)
async def update_rule(body: RuleTemplate):
    pass


@template_router.delete("/{template_id}", response_model=int)
async def delete_template():
    pass
