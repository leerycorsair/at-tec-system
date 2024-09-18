from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.store.postgres.session import get_db
from src.dto.db.editor.function import FunctionDB, FunctionParameterDB
from src.schema.function import Function, FunctionParameter


class FunctionRepository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db_session = db_session

    async def create_function(self, function: FunctionDB) -> int:
        try:
            new_function = Function(
                name=function.name,
                ret_type=function.ret_type,
                body=function.body,
                model_id=function.model_id,
            )

            self.db_session.add(new_function)
            self.db_session.commit()
            self.db_session.refresh(new_function)

            new_function_parameters = [
                FunctionParameter(
                    name=param.name,
                    type=param.type,
                    function_id=new_function.id,
                )
                for param in function.params
            ]

            self.db_session.add_all(new_function_parameters)
            self.db_session.commit()
            return new_function.id

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to create function: {e}")

    async def get_function(self, function_id: int) -> Optional[FunctionDB]:
        try:
            function = (
                self.db_session.query(Function)
                .filter(Function.id == function_id)
                .first()
            )
            if not function:
                return None

            parameters = (
                self.db_session.query(FunctionParameter)
                .filter(FunctionParameter.function_id == function_id)
                .all()
            )

            function_db = FunctionDB(
                id=function.id,
                name=function.name,
                ret_type=function.ret_type,
                body=function.body,
                model_id=function.model_id,
                params=[
                    FunctionParameterDB(
                        id=param.id,
                        name=param.name,
                        type=param.type,
                        function_id=param.function_id,
                    )
                    for param in parameters
                ],
            )

            return function_db

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get function: {e}")

    async def get_functions(self, model_id: int) -> List[FunctionDB]:
        try:
            functions = (
                self.db_session.query(Function)
                .filter(Function.model_id == model_id)
                .all()
            )

            functions_db = []
            for function in functions:
                parameters = (
                    self.db_session.query(FunctionParameter)
                    .filter(FunctionParameter.function_id == function.id)
                    .all()
                )
                functions_db.append(
                    FunctionDB(
                        id=function.id,
                        name=function.name,
                        ret_type=function.ret_type,
                        body=function.body,
                        model_id=function.model_id,
                        params=[
                            FunctionParameterDB(
                                id=param.id,
                                name=param.name,
                                type=param.type,
                                function_id=param.function_id,
                            )
                            for param in parameters
                        ],
                    )
                )

            return functions_db

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get functions: {e}")

    async def update_function(self, function: FunctionDB) -> FunctionDB:
        try:
            existing_function = (
                self.db_session.query(Function)
                .filter(Function.id == function.id)
                .first()
            )

            if not existing_function:
                raise RuntimeError("Function not found")

            existing_function.name = function.name
            existing_function.ret_type = function.ret_type
            existing_function.body = function.body
            existing_function.model_id = function.model_id

            self.db_session.commit()

            for param in function.params:
                existing_param = (
                    self.db_session.query(FunctionParameter)
                    .filter(FunctionParameter.id == param.id)
                    .first()
                )

                if existing_param:
                    existing_param.name = param.name
                    existing_param.type = param.type
                else:
                    new_param = FunctionParameter(
                        name=param.name,
                        type=param.type,
                        function_id=function.id,
                    )
                    self.db_session.add(new_param)

            self.db_session.commit()

            return function

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to update function: {e}")

    async def delete_function(self, function_id: int) -> None:
        try:
            function = (
                self.db_session.query(Function)
                .filter(Function.id == function_id)
                .first()
            )

            if not function:
                raise RuntimeError("Function not found")

            self.db_session.delete(function)
            self.db_session.commit()

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to delete function: {e}")
