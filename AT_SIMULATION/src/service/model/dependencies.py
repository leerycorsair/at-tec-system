from typing import List, Protocol

from fastapi import Depends

from src.repository.model.models.models import ModelMetaDB
from src.repository.model.repository import ModelRepository
from src.storage.postgres.session import get_db


class IModelRepository(Protocol):
    def create_model(self, model: ModelMetaDB) -> int: ...

    def get_model_meta(self, model_id: int) -> ModelMetaDB: ...

    def get_models(self, user_id: int) -> List[ModelMetaDB]: ...

    def update_model(self, model: ModelMetaDB) -> int: ...

    def delete_model(self, model_id: int) -> int: ...


def get_model_repository(session = Depends(get_db)) -> IModelRepository:
    return ModelRepository(session)
