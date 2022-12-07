import uuid

from sqlalchemy import Table, Column, ForeignKey

from db.orm import db_engine as db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Enum

from models.role import RoleModel


resource_role_table = Table(
    "resource_role_table",
    db.Model.metadata,
    Column("resources", ForeignKey("resources.id")),
    Column("roles", ForeignKey("roles.id")),
    Column("action", Enum("view", "delete", "edit", name='resource_action'))
)


class ResourceModel(db.Model):
    __tablename__ = 'resources'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False,
                   )

    name = db.Column(db.String, unique=False, nullable=False)

    role: Mapped[list[RoleModel]] = relationship('RoleModel', secondary=resource_role_table)
