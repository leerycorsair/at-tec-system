from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from src.schema.base import Base
from sqlalchemy.orm import relationship


class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    ret_type = Column(String, nullable=False)
    body = Column(Text, nullable=False)

    parameters = relationship("FunctionParameter", cascade="all, delete-orphan")
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_function_name_model_id",
        ),
    )


class FunctionParameter(Base):
    __tablename__ = "function_parameters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    function_id = Column(Integer, ForeignKey("functions.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "function_id",
            name="uix_function_parameter_function",
        ),
    )
