from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

frontend_router = APIRouter()

CWD_PATH = Path(os.getcwd()).resolve()

FRONTEND_BUILD_PATH = os.path.join(CWD_PATH, 'frontend/build')

templates = Jinja2Templates(directory=FRONTEND_BUILD_PATH)

@frontend_router.get("/{path:path}")
async def serve_frontend(request: Request, path: str):
    return templates.TemplateResponse("index.html", {"request": request})