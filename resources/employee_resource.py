

from flask_restful import Resource, reqparse
from models import db, Employee
from flask import jsonify

class EmployeeListResource(Resource):
    def get(self):
        try:
            employees = Employee.query.all()
           
            return jsonify([employee.to_dict() for employee in employees])
        except Exception as e:
            
            print(f"Error fetching employees: {e}")
            import traceback
            traceback.print_exc() 
            return {'message': 'Internal Server Error'}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('employeeId', type=str, required=True, help='Employee ID is required')
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('department', type=str, required=True, help='Department is required')
        parser.add_argument('profilePic', type=str, required=False)
        parser.add_argument('role', type=str, required=False)
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('phone', type=str, required=False)
        parser.add_argument('hireDate', type=str, required=True, help='Hire Date is required (YYYY-MM-DD)')
        parser.add_argument('currentStatus', type=str, required=False)
        args = parser.parse_args()

        try:
            
            from datetime import datetime
            args['hireDate'] = datetime.strptime(args['hireDate'], '%Y-%m-%d').date()

            new_employee = Employee(**args)
            db.session.add(new_employee)
            db.session.commit()
            return new_employee.to_dict(), 201
        except Exception as e:
            print(f"Error creating employee: {e}")
            import traceback
            traceback.print_exc()
            return {'message': 'Error creating employee'}, 500

class EmployeeResource(Resource):
    def get(self, employee_id):
        employee = Employee.query.filter_by(employeeId=employee_id).first()
        if not employee:
            return {'message': 'Employee not found'}, 404
        return employee.to_dict(), 200

    def put(self, employee_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('department', type=str, required=False)
        parser.add_argument('profilePic', type=str, required=False)
        parser.add_argument('role', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        parser.add_argument('phone', type=str, required=False)
        parser.add_argument('hireDate', type=str, required=False)
        parser.add_argument('currentStatus', type=str, required=False)
        args = parser.parse_args()

        employee = Employee.query.filter_by(employeeId=employee_id).first()
        if not employee:
            return {'message': 'Employee not found'}, 404

        try:
            for key, value in args.items():
                if value is not None:
                    
                    if key == 'hireDate':
                        from datetime import datetime
                        setattr(employee, key, datetime.strptime(value, '%Y-%m-%d').date())
                    else:
                        setattr(employee, key, value)
            db.session.commit()
            return employee.to_dict(), 200
        except Exception as e:
            print(f"Error updating employee: {e}")
            import traceback
            traceback.print_exc()
            return {'message': 'Error updating employee'}, 500

    def delete(self, employee_id):
        employee = Employee.query.filter_by(employeeId=employee_id).first()
        if not employee:
            return {'message': 'Employee not found'}, 404

        try:
            db.session.delete(employee)
            db.session.commit()
            return {'message': 'Employee deleted'}, 204
        except Exception as e:
            print(f"Error deleting employee: {e}")
            import traceback
            traceback.print_exc()
            return {'message': 'Error deleting employee'}, 500