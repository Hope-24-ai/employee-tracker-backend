from flask import Blueprint, jsonify
from app.models.employee import Employee
from app.db import db

employee_routes = Blueprint('employee_routes', __name__)

@employee_routes.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])
