from marshmallow import Schema, fields, validate
from app.utils import ROLES

class SignupSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    role = fields.Str(validate=validate.OneOf(ROLES), load_default="user")

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)