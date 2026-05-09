from marshmallow import Schema, fields, validate


class CreateTaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    description = fields.Str(validate=validate.Length(max=1000), allow_none=True)
    assigned_to_id = fields.UUID(allow_none=True)


class TaskSchema(Schema):
    task_id = fields.UUID(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    created_by_id = fields.UUID()
    assigned_to_id = fields.UUID(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UpdateTaskSchema(Schema):
    title = fields.Str(validate=validate.Length(min=3, max=150))
    description = fields.Str(validate=validate.Length(max=1000), allow_none=True)
    status = fields.Str(validate=validate.OneOf(["pending", "in_progress", "completed"]))
    assigned_to_id = fields.UUID(allow_none=True)
