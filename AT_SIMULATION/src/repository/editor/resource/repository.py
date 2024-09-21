from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.repository.editor.resource.models.conversions import (
    to_Resource,
    to_ResourceAttribute,
    to_ResourceAttributeDB,
    to_ResourceDB,
    to_ResourceType,
    to_ResourceTypeAttribute,
    to_ResourceTypeAttributeDB,
    to_ResourceTypeDB,
)
from src.repository.editor.resource.models.models import (
    ResourceDB,
    ResourceTypeDB,
)
from src.schema.resource import (
    ResourceType,
    ResourceTypeAttribute,
    Resource,
    ResourceAttribute,
)
from src.store.postgres.session import get_db


class ResourceRepository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db_session = db_session

    async def create_resource_type(self, resource_type: ResourceTypeDB) -> int:
        try:
            new_resource_type = to_ResourceType(resource_type)

            self.db_session.add(new_resource_type)
            self.db_session.commit()
            self.db_session.refresh(new_resource_type)

            new_resource_types_attributes = [
                to_ResourceTypeAttribute(attr) for attr in resource_type.attributes
            ]

            self.db_session.add_all(new_resource_types_attributes)
            self.db_session.commit()
            return new_resource_type.id

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to create resource type: {e}")

    async def get_resource_type(
        self, resource_type_id: int
    ) -> Optional[ResourceTypeDB]:
        try:
            resource_type = (
                self.db_session.query(ResourceType)
                .filter(ResourceType.id == resource_type_id)
                .first()
            )
            if not resource_type:
                return None

            attributes = (
                self.db_session.query(ResourceTypeAttribute)
                .filter(ResourceTypeAttribute.resource_type_id == resource_type_id)
                .all()
            )

            return to_ResourceTypeDB(resource_type, attributes)

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get resource type: {e}")

    async def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]:
        try:
            resource_types = (
                self.db_session.query(ResourceType)
                .filter(ResourceType.model_id == model_id)
                .all()
            )

            resource_types_db = []
            for resource_type in resource_types:
                attributes = (
                    self.db_session.query(ResourceTypeAttribute)
                    .filter(ResourceTypeAttribute.resource_type_id == resource_type.id)
                    .all()
                )
                resource_types_db.append(to_ResourceTypeDB(resource_type, attributes))

            return resource_types_db

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get resource types: {e}")

    async def update_resource_type(
        self, resource_type: ResourceTypeDB
    ) -> ResourceTypeDB:
        try:
            existing_resource_type = (
                self.db_session.query(ResourceType)
                .filter(ResourceType.id == resource_type.id)
                .first()
            )

            if not existing_resource_type:
                raise RuntimeError("Resource type not found")

            existing_resource_type.name = resource_type.name
            existing_resource_type.type = resource_type.type
            existing_resource_type.model_id = resource_type.model_id

            self.db_session.commit()

            for attr in resource_type.attributes:
                existing_attr = (
                    self.db_session.query(ResourceTypeAttribute)
                    .filter(ResourceTypeAttribute.id == attr.id)
                    .first()
                )

                if existing_attr:
                    existing_attr.name = attr.name
                    existing_attr.type = attr.type
                    existing_attr.default_value = attr.default_value
                else:
                    self.db_session.add(to_ResourceTypeAttribute(attr))

            self.db_session.commit()

            return resource_type

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to update resource type: {e}")

    async def delete_resource_type(self, resource_type_id: int) -> None:
        try:
            resource_type = (
                self.db_session.query(ResourceType)
                .filter(ResourceType.id == resource_type_id)
                .first()
            )

            if not resource_type:
                raise RuntimeError("Resource type not found")

            self.db_session.delete(resource_type)
            self.db_session.commit()

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to delete resource type: {e}")

    async def create_resource(self, resource: ResourceDB) -> int:
        try:
            new_resource = to_Resource(resource)

            self.db_session.add(new_resource)
            self.db_session.commit()
            self.db_session.refresh(new_resource)

            new_resource_types_attributes = [
                to_ResourceAttribute(attr, new_resource.id)
                for attr in resource.attributes
            ]

            self.db_session.add_all(new_resource_types_attributes)
            self.db_session.commit()
            return new_resource.id

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to create resource type: {e}")

    async def get_resource(self, resource_id: int) -> Optional[ResourceDB]:
        try:
            resource = (
                self.db_session.query(Resource)
                .filter(Resource.id == resource_id)
                .first()
            )
            if not resource:
                return None

            attributes = (
                self.db_session.query(ResourceAttribute)
                .filter(ResourceAttribute.resource_id == resource.id)
                .all()
            )

            return to_ResourceDB(resource, attributes)

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get resource: {e}")

    async def get_resources(self, model_id: int) -> List[ResourceDB]:
        try:
            resources = (
                self.db_session.query(Resource)
                .filter(Resource.model_id == model_id)
                .all()
            )

            resources_db = []
            for resource in resources:
                attributes = (
                    self.db_session.query(ResourceAttribute)
                    .filter(ResourceAttribute.resource_id == resource.id)
                    .all()
                )
                resources_db.append(to_ResourceDB(resource, attributes))

            return resources_db

        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to get resources: {e}")

    async def update_resource(self, resource: ResourceDB) -> ResourceDB:
        try:
            existing_resource = (
                self.db_session.query(Resource)
                .filter(Resource.id == resource.id)
                .first()
            )

            if not existing_resource:
                raise RuntimeError("Resource not found")

            existing_resource.name = resource.name
            existing_resource.to_be_traced = resource.to_be_traced
            existing_resource.resource_type_id = resource.type
            existing_resource.model_id = resource.model_id

            self.db_session.commit()

            for attr in resource.attributes:
                existing_attr = (
                    self.db_session.query(ResourceAttribute)
                    .filter(ResourceAttribute.id == attr.id)
                    .first()
                )

                if existing_attr:
                    existing_attr.value = attr.value
                else:
                    self.db_session.add(to_ResourceAttribute(attr, resource.id))

            self.db_session.commit()

            return resource

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to update resource: {e}")

    async def delete_resource(self, resource_id: int) -> None:
        try:
            resource = (
                self.db_session.query(Resource)
                .filter(Resource.id == resource_id)
                .first()
            )

            if not resource:
                raise RuntimeError("Resource not found")

            self.db_session.delete(resource)
            self.db_session.commit()

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to delete resource: {e}")