from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class AdminSchema(Schema):
    id = fields.Int(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class AdminResponseDataSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)


class AdminResponseSchema(OkResponseSchema):
    data = fields.Nested(AdminResponseDataSchema)