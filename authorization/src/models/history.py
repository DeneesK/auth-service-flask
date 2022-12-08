import datetime
import uuid

from db.orm import db_engine as db
from sqlalchemy.dialects.postgresql import UUID


class HistoryModel(db.Model):
    __tablename__ = 'access_history'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    device = db.Column(db.String, nullable=False)
    access_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class UserHistory(db.Model):
    __tablename__ = 'user_history'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    access_history_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('access_history.id')
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
