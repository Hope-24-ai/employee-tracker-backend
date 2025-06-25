# resources/employee_resource.py
from flask_restful import Resource
from models import db, Employee
from flask import request

class EmployeeListResource(Resource):
    def get(self):
        employees = Employee.query.all()
        return [ { "id": e.id, "employeeId": e.employeeId, "name": e.name, "department": e.department } for e in employees ], 200

    def post(self):
        data = request.get_json()
        employee = Employee(employeeId=data["employeeId"], name=data["name"], department=data["department"])
        db.session.add(employee)
        db.session.commit()
        return {"message": "Employee added"}, 201
