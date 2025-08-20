from marshmallow import fields, validate
from .extensions import ma


class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    role = fields.Str(dump_only=True)


class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class ItemSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    description = fields.Str(load_default='')
    owner_id = fields.Int(dump_only=True)