from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from models.resource import ResourceModel
#from models.role import RoleModel
#from models.resource_role import ResourceRole

ResourceModel.permission = relationship('ResourceRole', back_populates='resource')
ResourceModel.roles = association_proxy('permission', 'role')
