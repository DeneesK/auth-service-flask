from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.user import UserModel


class Data(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ('password',)


user_data = Data()
