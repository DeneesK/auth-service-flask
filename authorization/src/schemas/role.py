from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from models.resource import ResourceModel
from models.role import RoleModel
from models.resource_role import ResourceRoleModel


ResourceModel.permission = relationship(ResourceRoleModel, back_populates='resource')
ResourceModel.roles = association_proxy('permission', 'role')  # tables are created - with or without

print('Set RoleModel.permission')
RoleModel.permission = relationship(ResourceRoleModel, back_populates='role')
print('After Set RoleModel.permission')
RoleModel.resources = association_proxy('permission', 'resource')  # tables are created - with or without


class RoleData(SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel


role_data = RoleData()
