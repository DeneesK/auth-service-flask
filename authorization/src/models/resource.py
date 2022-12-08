import uuid

from db.orm import db_engine as db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Enum
from sqlalchemy.ext.associationproxy import association_proxy

from models.role import RoleModel


class ResourceModel(db.Model):
    __tablename__ = 'resources'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False,
                   )

    name = db.Column(db.String,
                     unique=False,
                     nullable=False)

    permission: Mapped[list[RoleModel]] = relationship('ResourceRole',
                                                       back_populates='resource')
    roles = association_proxy('permission', 'role')


class ResourceRole(db.Model):
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
