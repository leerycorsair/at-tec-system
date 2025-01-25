from typing import List, Protocol

from fastapi import Depends, Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.client.auth_client import AuthClientSingleton
from src.repository.model.models.models import ModelMetaDB
from src.service.model.dependencies import (IModelRepository,
                                            get_function_service,
                                            get_model_repository,
                                            get_resource_service,
                                            get_template_service)
from src.service.model.service import ModelService

bearer_scheme = HTTPBearer()


class IModelService(Protocol):
    def check_model_rights(self, model_id: int, user_id: int) -> None: ...

    def create_model(self, model: ModelMetaDB) -> int: ...

    def get_models(self, user_id: int) -> List[ModelMetaDB]: ...

    def update_model(self, model: ModelMetaDB) -> int: ...

    def delete_model(self, model_id: int, user_id: int) -> int: ...


def get_model_service(
    model_rep: IModelRepository = Depends(get_model_repository),
    resource_service=Depends(get_resource_service),
    template_service=Depends(get_template_service),
    function_service=Depends(get_function_service),
) -> IModelService:
    return ModelService(
        model_rep,
        resource_service,
        template_service,
        function_service,
    )


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
    model_service: IModelService = Depends(get_model_service),
) -> int:
    if not model_id:
        raise HTTPException(status_code=400, detail="model_id header is missing")

    model_service.check_model_rights(model_id, user_id)
    return model_id
