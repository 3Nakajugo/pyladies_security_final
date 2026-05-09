from app.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


# app/models/task_model.py
class Task(db.Model):

    __tablename__ = "tasks"

    task_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default="pending")
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=True)
    assigned_to_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
        backref="created_tasks"
    )
    assigned_to = db.relationship(
        "User",
        foreign_keys=[assigned_to_id],
        backref="assigned_tasks"
    )
