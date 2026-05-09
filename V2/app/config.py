import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_POSTGRESQL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT=os.getenv("PORT", 5001)
    FLASK_ENV=os.getenv("FLASK_ENV", "production")
    BASE_URL=os.getenv("BASE_URL", "api/v1")
