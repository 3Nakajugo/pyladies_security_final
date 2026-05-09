from app.extensions import db
from app.models import TokenBlocklist

def revoke_token(jti):
    try:
        token = TokenBlocklist(jti=jti)
        db.session.add(token)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e