from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from models.resource import ResourceModel
#from models.resource_role import ResourceRoleModel

#ResourceModel.permission = relationship(ResourceRoleModel, back_populates='resource')
#ResourceModel.roles = association_proxy('permission', 'role')  # tables are created - with or without


class ResourceData(SQLAlchemyAutoSchema):
    class Meta:
        model = ResourceModel


resource_data = ResourceData()
