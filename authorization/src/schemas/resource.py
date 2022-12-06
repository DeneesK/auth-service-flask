from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.resource import ResourceModel


class ResourceData(SQLAlchemyAutoSchema):
    class Meta:
        model = ResourceModel


resource_data = ResourceData()
