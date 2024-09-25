from abc import ABC, abstractmethod
from typing import List
from fastapi import Depends, Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.client.auth_client import AuthClientSingleton


from src.repository.model.models.models import (
    CreateModelParamsDB,
    ModelMetaDB,
    UpdateModelParamsDB,
)
from src.service.model.service import ModelService


bearer_scheme = HTTPBearer()


class IModelService(ABC):
    @abstractmethod
    async def check_rights(self, model_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    async def create_model(
        self, user_id: int, params: CreateModelParamsDB
    ) -> ModelMetaDB:
        pass

    # @abstractmethod
    # async def get_model(self, model_id: int) -> service.Model:
    #     pass

    @abstractmethod
    async def get_models(self, user_id: int) -> List[ModelMetaDB]:
        pass

    @abstractmethod
    async def update_model(
        self, model_id: int, params: UpdateModelParamsDB
    ) -> ModelMetaDB:
        pass

    @abstractmethod
    async def delete_model(self, model_id: int) -> ModelMetaDB:
        pass


def get_model_service() -> IModelService:
    return ModelService()


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
    return model_id
