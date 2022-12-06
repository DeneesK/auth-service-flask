import uuid

from db.orm import db_engine as db
from sqlalchemy.dialects.postgresql import UUID


class ResourceModel(db.Model):
    __tablename__ = 'resources'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False,
                   )

    name = db.Column(db.String, unique=False, nullable=False)

