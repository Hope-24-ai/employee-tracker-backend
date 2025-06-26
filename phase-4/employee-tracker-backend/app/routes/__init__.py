# ✅ Correct if route files are in app/ directly
from . import employee_routes, department_routes, review_routes, dashboard_routes
from flask import Flask
from app.models import Admin, Employee, Department


from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Make sure this exists

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Admin  # import your models so Flask-Migrate can find them

    return app




