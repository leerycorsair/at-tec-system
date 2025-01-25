from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Import(Base):
    __tablename__ = "imports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    packages = relationship("Package", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_import_name_model_id",
        ),
    )


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    alias = Column(String, nullable=True)

    import_id = Column(Integer, ForeignKey("imports.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "import_id",
            name="uix_package_name_import_id",
        ),
        UniqueConstraint(
            "alias",
            "import_id",
            name="uix_package_alias_import_id",
        ),
    )
