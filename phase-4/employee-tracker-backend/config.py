# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///employee.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super-secret'  # Replace this with a secure key in production
