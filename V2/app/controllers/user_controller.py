from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from app.schemas import SignupSchema, LoginSchema, UserSchema
from app.services import register_user, login_user, logout_user, get_user_profile


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def register():
    try:
        data = SignupSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({
            "message": "Validation failed",
            "errors": err.messages
        }), 400

    response, status_code = register_user(data)
    return jsonify(response), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = LoginSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({
            "message": "Validation failed",
            "errors": err.messages
        }), 400

    response, status_code = login_user(data)
    return jsonify(response), status_code

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response, status_code = logout_user()
    return jsonify(response), status_code


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    response, status_code = get_user_profile()
    return jsonify(response), status_code
