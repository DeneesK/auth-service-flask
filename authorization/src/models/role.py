import uuid

from db.orm import db_engine as db
from sqlalchemy.dialects.postgresql import UUID


class RoleModel(db.Model):
    __tablename__ = 'roles'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String, unique=True, nullable=False)
    client_service_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'
