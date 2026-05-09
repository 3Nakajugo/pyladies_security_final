
def user_create_response(user):
    return {
        "id": user.user_id,
        "full_name": user.name,
        "email": user.email,
        "role": user.role,
        "password": user.password_hash
    }