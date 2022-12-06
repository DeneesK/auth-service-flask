from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.user import UserModel
from models.role import RoleModel
from models.resource import ResourceModel


class UserData(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ('password',)


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
