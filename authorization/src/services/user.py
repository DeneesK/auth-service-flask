"""The service won't handle errors itself, API does it."""
import random

from db.orm import db_engine
from models import UserRoleModel
from models.user import UserModel
from pbkdf2 import crypt

from services.role import RoleService
from .exceptions import ObjectNotFoundException


def random_string(length):
    def random_char():
        return chr(random.randint(ord('a'), ord('z')))

    return ''.join(random_char() for _ in range(length))


class UserService:
    password_hash_iterations = 100

    def create(self, login, password, commit=True) -> UserModel:
        """We hash the password here.
        :returns: Success or not"""
        hashed_password = crypt(
            password,
            '.' + random_string(random.randint(10, 20)),
            iterations=self.password_hash_iterations,
        )
        new_user = UserModel(login=login, password=hashed_password)
        db_engine.session.add(new_user)
        if commit:
            db_engine.session.commit()
        return new_user

    def get(self, user_id) -> UserModel:
        obj = UserModel.query.get(user_id)
        if not obj:
            raise ObjectNotFoundException('User', user_id)
        return obj

    def all(self) -> list[UserModel]:
        return UserModel.query.all()

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

    def assign_role(self, user_id, role_id):
        self.get(user_id)  # Check that the user exists
        role_service = RoleService()
        role_service.get(role_id)  # Check that the role exists
        user_role = UserRoleModel.get(user_id=user_id, role_id=role_id)
        db_engine.session.add(user_role)
        # user_obj.roles.append(role_obj) <- doesn't work
        db_engine.session.commit()

    def revoke_role(self, user_id, role_id):
        user_role = UserRoleModel.query.filter_by(user_id=user_id, role_id=role_id).all()
        if user_role:
            for itm in user_role:
                db_engine.session.delete(itm)
        else:
            raise ObjectNotFoundException('Role for user', role_id)
