from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    UniqueConstraint,
)
from .base import Base
from sqlalchemy.orm import relationship


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    nodes = relationship("Node", cascade="all, delete-orphan")
    edges = relationship("Edge", cascade="all, delete-orphan")
    resource_types = relationship("ResourceType", cascade="all, delete-orphan")
    resources = relationship("Resource", cascade="all, delete-orphan")
    functions = relationship("Function", cascade="all, delete-orphan")
    templates = relationship("Template", cascade="all, delete-orphan")
    template_usages = relationship("TemplateUsage", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint(
            "name",
            "user_id",
            name="uix_model_name_user_id",
        ),
    )
