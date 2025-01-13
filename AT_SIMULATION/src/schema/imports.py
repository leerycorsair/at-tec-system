from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship


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
    import_ = relationship("Import", back_populates="packages")

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
        UniqueConstraint(
            "alias",
            "import_.model_id",
            name="uix_package_alias_model_id",
        ),
    )
