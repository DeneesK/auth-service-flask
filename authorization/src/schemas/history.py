from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from models.history import HistoryModel


class HistoryData(SQLAlchemyAutoSchema):
    class Meta:
        model = HistoryModel


history_data = HistoryData()


class AccessSchema(Schema):
    access_date = fields.Str()
    device = fields.Str()


class HistorySchema(Schema):
    user_history = fields.List(fields.Nested(AccessSchema()))


history_schema = HistorySchema()
