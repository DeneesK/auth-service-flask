from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from models.resource_role import ResourceRoleModel


class ResourceRoleData(SQLAlchemyAutoSchema):
    class Meta:
        model = ResourceRoleModel


resource_role_data = ResourceRoleData()
