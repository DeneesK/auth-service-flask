import uuid

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from db.orm import db_engine as db
from models.resource import ResourceModel


class ResourceRoleModel(db.Model):
    """Links resource and role and action"""
    __tablename__ = 'resource_role_table'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False,
                   )
    resource_id = db.Column(UUID(as_uuid=True),
                            db.ForeignKey('resources.id'))

    role_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('roles.id'))

    action = db.Column(Enum('view', 'delete', 'edit', name='resource_action', create_type=True))

    resource = db.relationship(ResourceModel,
                               back_populates='permission')
