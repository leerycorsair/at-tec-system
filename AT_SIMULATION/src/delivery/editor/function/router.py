from typing import List
from fastapi import APIRouter
from src.dto.api.editor.function import Function

function_router = APIRouter(
    prefix="/functions",
    tags=["editor:functions"],
)


@function_router.post("/", response_model=int)
async def create_function(body: Function):
    pass


@function_router.get("/", response_model=List[Function])
async def get_functions():
    pass


@function_router.get("/{function_id}", response_model=Function)
async def get_function():
    pass


@function_router.put("/{function_id}", response_model=int)
async def update_function(body: Function):
    pass


@function_router.delete("/{function_id}", response_model=int)
async def delete_function():
    pass
