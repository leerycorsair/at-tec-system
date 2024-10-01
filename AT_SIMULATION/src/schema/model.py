from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    UniqueConstraint,
)
from .base import Base


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    __table_args__ = (
        UniqueConstraint(
            "name",
            "user_id",
            name="uix_model_name_user_id",
        ),
    )
