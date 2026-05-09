from flask import Flask
from .extensions import db, migrate, jwt
from app.config import Config
from app.controllers import auth_bp, task_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app import models  # Import models to register them with SQLAlchemy

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    from app.models import TokenBlocklist

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None #returns true or flase depending on whether the token is found in the blocklist

    app.register_blueprint(auth_bp, url_prefix=f"/{Config.BASE_URL}/auth")
    app.register_blueprint(task_bp, url_prefix=f"/{Config.BASE_URL}/tasks")

    return app
