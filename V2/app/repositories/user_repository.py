from app.models.user_model import User
from app.extensions import db

def find_user_by_email(email):
    return User.query.filter_by(email=email).first()

def find_user_by_id(user_id):
    return User.query.filter_by(user_id=user_id).first()

def create_user(name, email, password_hash, role):
    try:
        name = name.strip()
        email = email.strip().lower()
        password_hash = password_hash.strip()
        role = role.strip().lower()

        user = User(name=name, email=email, password_hash=password_hash, role=role)

        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e

  

