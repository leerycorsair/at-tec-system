from fastapi import Depends, Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.client.auth_client import AuthClientSingleton


import asyncio

from src.service.model.model import ModelService

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> int:
    token = credentials.credentials

    try:
        auth_client = await AuthClientSingleton.get_instance()
        user_id = await auth_client.verify_token(token)
    except Exception as e:
        raise HTTPException(status_code=500, detail="token verification failed") from e

    return user_id


async def get_current_model(
    model_id: int = Header(...),
    user_id: int = Depends(get_current_user),
    model_service: ModelService = Depends(),
):
    if not model_id:
        raise HTTPException(status_code=400, detail="model_id header is missing")

    return await model_service.check_rights(model_id, user_id)


async def check_model_rights(
    model_id: int,
    user_id: int = Depends(get_current_user),
    model_service: ModelService = Depends(),
):
    await model_service.check_rights(model_id, user_id)
