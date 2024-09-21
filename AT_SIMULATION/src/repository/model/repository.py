from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .models.conversions import to_ModelMetaDB
from .models.models import (
    CreateModelParamsDB,
    ModelMetaDB,
    UpdateModelParamsDB,
)
from src.schema.model import Model
from src.store.postgres.session import get_db


class ModelRepository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db_session = db_session

    async def create_model(self, model: CreateModelParamsDB) -> ModelMetaDB:
        new_model = Model(
            name=model.name,
            user_id=model.user_id,
        )
        self.db_session.add(new_model)
        self.db_session.commit()
        self.db_session.refresh(new_model)
        return to_ModelMetaDB(model)

    async def get_model_short(self, model_id: int) -> ModelMetaDB:
        existing_model = self.db_session.query(Model).filter_by(id=model_id).first()
        if not existing_model:
            raise ValueError(f"Model with id {model_id} does not exist")
        self.db_session.commit()
        self.db_session.refresh(existing_model)
        return to_ModelMetaDB(existing_model)

    async def get_models(self, user_id: int) -> List[ModelMetaDB]:
        models = self.db_session.query(Model).filter_by(user_id=user_id).all()

        if not models:
            return []

        return [to_ModelMetaDB(model) for model in models]

    async def update_model(
        self, model_id: int, params: UpdateModelParamsDB
    ) -> ModelMetaDB:
        existing_model = self.db_session.query(Model).filter_by(id=model_id).first()
        if not existing_model:
            raise ValueError(f"Model with id {model_id} does not exist")
        existing_model.name = params.name
        self.db_session.commit()
        self.db_session.refresh(existing_model)
        return to_ModelMetaDB(existing_model)

    async def delete_model(self, model_id: int) -> int:
        try:
            model_to_delete = self.db_session.query(Model).filter_by(id=model_id).one()
            self.db_session.delete(model_to_delete)
            self.db_session.commit()
            return model_id
        except NoResultFound:
            raise ValueError(f"Model with id {model_id} does not exist")
