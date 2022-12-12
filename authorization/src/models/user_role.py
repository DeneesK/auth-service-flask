import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.orm import db_engine as db

from models.role import RoleModel  # ok
from models.user import UserModel


class UserRoleModel(db.Model):
    """Links resource and role and action"""
    # TODO Add unique index for user_id/role_id.
    __tablename__ = 'user_role_table'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False,
                   )
    user_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('users.id'))

    role_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('roles.id'))
    __table_args__ = (db.Index('user_role_index', "user_id", "role_id"),)

    user = db.relationship(UserModel, back_populates='user_role')
    role = db.relationship(RoleModel, back_populates='user_role')
