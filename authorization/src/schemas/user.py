from flask_marshmallow.sqla import SQLAlchemyAutoSchema, auto_field
from models.user import UserModel
from models.role import RoleModel
from models.resource import ResourceModel


class UserData(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    password = auto_field(load_only=True)


class RoleData(SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel
        # exclude = #('password',)


class ResourceData(SQLAlchemyAutoSchema):
    class Meta:
        model = ResourceModel
        # exclude = ('password',)


user_data = UserData()
role_data = UserData()
resource_data = UserData()
