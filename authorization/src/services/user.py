"""The service won't handle errors itself, API does it."""
import random

from db.orm import db_engine
from models.user import UserModel
from pbkdf2 import crypt


def random_string(length):
    def random_char():
        return chr(random.randint(ord('a'), ord('z')))

    return ''.join(random_char() for _ in range(length))


class UserService:
    password_hash_iterations = 100

    def create(self, login, password) -> (bool, str):
        """We hash the password here.
        :returns: Success or not"""
        hashed_password = crypt(
            password,
            '.' + random_string(random.randint(10, 20)),
            iterations=self.password_hash_iterations,
        )
        new_user = UserModel(login=login, password=hashed_password)
        db_engine.session.add(new_user)
        db_engine.session.commit()
        return new_user

    def get(self, user_id) -> UserModel:
        return UserModel.query.get(user_id)
    
    def _delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            db_engine.session.delete(user)
            db_engine.session.commit()
            return True
        return False
