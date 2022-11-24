import uuid
from sqlalchemy.dialects.postgresql import UUID
from db.orm import engine as db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, login, password):
        super().__init__()
        self.login = login
        self.password = password

    def __repr__(self):
        return f'<User {self.login}>'
