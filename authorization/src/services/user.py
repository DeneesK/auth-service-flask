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

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            db_engine.session.delete(user)
            db_engine.session.commit()
            return True
        return False

    def get_by_credentials(self, login, password) -> UserModel:
        user = UserModel.query.filter(UserModel.login == login).one_or_none()
        if user and user.password == crypt(password, user.password):
            return user

    def change_password(self, user, new_password):
        hashed_password = crypt(
            new_password,
            '.' + random_string(random.randint(10, 20)),
            iterations=self.password_hash_iterations,
        )
        user.password = hashed_password
        db_engine.session.commit()
