# app/routes/login_route.py
from flask import request, jsonify, session
from werkzeug.security import check_password_hash
from app.models import db, Admin, Employee  # Update to your actual models

@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        # CORS preflight support
        response = jsonify({})
        response.status_code = 204
        return response

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Check Admin first
    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        session["user_id"] = admin.id
        session["role"] = "admin"
        return jsonify({
            "name": admin.name,
            "role": "admin",
            "greeting": f"Welcome back, {admin.name}!"
        }), 200

    # Then check Employee
    employee = Employee.query.filter_by(email=email).first()
    if employee and check_password_hash(employee.password, password):
        session["user_id"] = employee.id
        session["role"] = "employee"
        return jsonify({
            "name": employee.name,
            "role": "employee",
            "greeting": f"Hello {employee.name}!"
        }), 200

    # If not found or password wrong
    return jsonify({"error": "Invalid credentials"}), 401
