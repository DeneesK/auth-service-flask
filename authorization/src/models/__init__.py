from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from models.resource import ResourceModel
from models.resource_role import ResourceRoleModel
from models.role import RoleModel

ResourceModel.permission = relationship(ResourceRoleModel, back_populates='resource', cascade="all, delete")
ResourceModel.roles = association_proxy('permission', 'role')  # tables are created - with or without

RoleModel.permission = relationship(ResourceRoleModel, back_populates='role', cascade="all, delete")
RoleModel.resources = association_proxy('permission', 'resource')  # tables are created - with or without
