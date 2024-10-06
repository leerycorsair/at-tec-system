from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from src.repository.helper import handle_sqlalchemy_errors

from .models.conversions import to_Model, to_ModelMetaDB
from .models.models import CreateModelParamsDB, ModelMetaDB, UpdateModelParamsDB
from src.schema.model import Model
from src.store.postgres.session import get_db


class ModelRepository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db_session = db_session

    @handle_sqlalchemy_errors
    def create_model(self, model: CreateModelParamsDB) -> int:
        with self.db_session.begin():
            new_model = to_Model(model)
            self.db_session.add(new_model)
            self.db_session.refresh(new_model)
        return new_model.id

    @handle_sqlalchemy_errors
    def get_model_meta(self, model_id: int) -> ModelMetaDB:
        model = self._get_model_by_id(model_id)
        return to_ModelMetaDB(model)

    @handle_sqlalchemy_errors
    def get_models(self, user_id: int) -> List[ModelMetaDB]:
        models = self.db_session.query(Model).filter_by(user_id=user_id).all()
        return [to_ModelMetaDB(model) for model in models]

    @handle_sqlalchemy_errors
    def update_model(self, model_id: int, params: UpdateModelParamsDB) -> int:
        with self.db_session.begin():
            model = self._get_model_by_id(model_id)
            model.name = params.name
        return model_id

    @handle_sqlalchemy_errors
    def delete_model(self, model_id: int) -> int:
        with self.db_session.begin():
            model = self._get_model_by_id(model_id)
            self.db_session.delete(model)
        return model_id

    def _get_model_by_id(self, model_id: int) -> Model:
        model = self.db_session.query(Model).filter_by(id=model_id).one_or_none()
        if not model:
            raise ValueError(f"Model with id {model_id} does not exist")
        return model
