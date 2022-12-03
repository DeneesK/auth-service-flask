from flask_marshmallow.sqla import SQLAlchemyAutoSchema, auto_field
from models.user import UserModel


class Data(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    password = auto_field(load_only=True)


user_data = Data()
