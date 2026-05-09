from datetime import timedelta

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity
from app.repositories import find_user_by_email, create_user, revoke_token, find_user_by_id
from app.utils import hash_password, check_password_hash, random_number_generator
from app.views import user_create_response



def register_user(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")  # Default role is 'user' if not provided

    if not name or not email or not password:
        return {"message": "All fields are required"}, 400

    existing_user = find_user_by_email(email)

    if existing_user:
        return {"message": "Email already exists"}, 400
    
    password_hash = hash_password(password)

    user = create_user(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role
    )
    print(f"User created: {user_create_response(user)}")

    return {
        "message": "User registered successfully",
        "user": user_create_response(user)
    }, 201


def login_user(data):
    email = data.get("email")
    password = data.get("password")

    user = find_user_by_email(email)

    if not user:
        return {"message": "Invalid email or password"}, 401

    if not check_password_hash(user.password_hash, password):
        return {"message": "Invalid email or password"}, 401

    access_token = create_access_token(
        identity=str(user.user_id),
        additional_claims={"role": user.role, "name": user.name},
        expires_delta=timedelta(hours=24),
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user": user_create_response(user)
    }, 200


def logout_user():
    jwt_data = get_jwt()
    print(f"JWT data for logout: {jwt_data}")

    jti = jwt_data["jti"]

    revoke_token(jti)

    return {"message": "Logout successful"}, 200


def get_user_profile():
    user_id = get_jwt_identity()
    user = find_user_by_id(user_id)
    
    if not user:
        return {"message": "User not found"}, 404
    
    return {
        "message": "Profile retrieved successfully",
        "user": {
            "id": str(user.user_id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    }, 200