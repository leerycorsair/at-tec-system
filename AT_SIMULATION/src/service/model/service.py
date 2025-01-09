from typing import List

from src.repository.model.models.models import ModelMetaDB
from src.service.model.dependencies import IModelRepository


class ModelService:
    def __init__(
        self,
        model_rep: IModelRepository,
    ) -> None:
        self._model_rep = model_rep

    def check_model_rights(self, model_id: int, user_id: int) -> None:
        model = self._model_rep.get_model_meta(model_id)
        if model.user_id != user_id:
            raise ValueError(f"Model {model_id} does not belong to user {user_id}")

    def create_model(self, model: ModelMetaDB) -> int:
        return self._model_rep.create_model(model)

    def get_models(self, user_id: int) -> List[ModelMetaDB]:
        return self._model_rep.get_models(user_id)

    def update_model(self, model: ModelMetaDB) -> int:
        self.check_model_rights(model.id, model.user_id)
        return self._model_rep.update_model(model)

    def delete_model(self, model_id: int, user_id: int) -> int:
        self.check_model_rights(model_id, user_id)
        return self._model_rep.delete_model(model_id)
