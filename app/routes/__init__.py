from flask import Blueprint

def register_routes(app):
    from .dashboard_routes import dashboard_routes
    from .employee_routes import employee_routes

    app.register_blueprint(dashboard_routes)
    app.register_blueprint(employee_routes)
