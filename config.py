import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Instance folder to store DB and other files
    INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
    os.makedirs(INSTANCE_DIR, exist_ok=True)

    # Database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")  # For sessions
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-jwt-key")  # For JWT auth
