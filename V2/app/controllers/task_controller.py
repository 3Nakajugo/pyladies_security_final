from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from app.utils import role_required
from app.schemas import CreateTaskSchema, UpdateTaskSchema
from app.services.task_service import (
    create_task_service,
    get_user_tasks_service,
    get_task_by_id_service,
    update_task_service,
    delete_task_service
)


task_bp = Blueprint("tasks", __name__)


@task_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required("admin")  # Only allow users with 'admin'
def create_task():
    """Create a new task"""
    try:
        data = CreateTaskSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({
            "message": "Validation failed",
            "errors": err.messages
        }), 400

    response, status_code = create_task_service(data)
    return jsonify(response), status_code


@task_bp.route("/get_tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    """Get all tasks for the authenticated user"""
    response, status_code = get_user_tasks_service()
    return jsonify(response), status_code


@task_bp.route("/<task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    """Get a specific task by ID"""
    response, status_code = get_task_by_id_service(task_id)
    return jsonify(response), status_code


@task_bp.route("/<task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """Update a task"""
    try:
        data = UpdateTaskSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({
            "message": "Validation failed",
            "errors": err.messages
        }), 400

    response, status_code = update_task_service(task_id, data)
    return jsonify(response), status_code


@task_bp.route("/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """Delete a task"""
    response, status_code = delete_task_service(task_id)
    return jsonify(response), status_code
