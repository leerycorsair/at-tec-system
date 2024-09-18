from fastapi import Depends
from sqlalchemy.orm import Session
from src.dto.db.user import DTOUserDB
from src.schema.user import User
from src.store.postgres.session import get_db


class UserRepository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db_session = db_session

    def create_user(self, user: DTOUserDB) -> int:
        new_user = User(
            login=user.login, password=user.password, email=user.email, group=user.group
        )
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        return new_user.id

    def get_user(self, login: str) -> DTOUserDB:
        user = self.db_session.query(User).filter_by(login=login).first()
        if user is not None:
            return DTOUserDB(
                id=user.id,
                login=user.login,
                password=user.password,
                email=user.email,
                group=user.group,
            )
        else:
            raise ValueError("User not found")
