from flask import Blueprint

# Assuming each route file defines a Blueprint like:
# employee_bp = Blueprint('employee_bp', __name__)
from app.routes.employee_routes import employee_bp
from app.routes.department_routes import department_bp
from app.routes.review_routes import review_bp
from app.routes.dashboard_routes import dashboard_bp

def register_routes(app):
    app.register_blueprint(employee_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(dashboard_bp)

