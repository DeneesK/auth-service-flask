from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from models.resource import ResourceModel
from models.resource_role import ResourceRoleModel
from models.role import RoleModel
from models.user import UserModel
from models.user_role import UserRoleModel

# Region Resoure/Role
ResourceModel.permission = relationship(ResourceRoleModel, back_populates='resource')
ResourceModel.roles = association_proxy('permission', 'role')  # tables are created - with or without

RoleModel.permission = relationship(ResourceRoleModel, back_populates='role')
RoleModel.resources = association_proxy('permission', 'resource')  # tables are created - with or without
# endregion

# Region User/Role
UserModel.user_role = relationship(UserRoleModel, back_populates='user')
UserModel.roles = association_proxy('user_role', 'role')  # tables are created - with or without

RoleModel.user_role = relationship(UserRoleModel, back_populates='role')
RoleModel.users = association_proxy('user_role', 'users')  # tables are created - with or without
# endregion
