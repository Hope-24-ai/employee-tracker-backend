

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, Employee, AttendanceRecord, LeaveRequest, Department 
import os
import traceback
from datetime import date, timedelta 


from resources.employee_resource import EmployeeListResource, EmployeeResource
from resources.attendance_resource import AttendanceListResource, AttendanceResource
from resources.leave_request_resource import LeaveRequestListResource, LeaveRequestResource
from resources.department_resource import DepartmentListResource

app = Flask(__name__, instance_relative_config=True)


database_path = os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    os.makedirs(app.instance_path)
    print(f"Created instance folder: {app.instance_path}")
except OSError as e:
    if e.errno == 17:
        print(f"Instance folder already exists: {app.instance_path}")
    else:
        print(f"Error creating instance folder: {e}")

db.init_app(app)
CORS(app)
api = Api(app)



with app.app_context():
    print("\n--- Starting Database Initialization ---")
    print(f"Database URI configured: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Instance path: {app.instance_path}")

    try:
        print("Attempting db.create_all()...")
        db.create_all()
        print("db.create_all() executed.")

        
        print("Checking for existing Departments...")
        hr_dept = db.session.query(Department).filter_by(name="Human Resources").first()
        eng_dept = db.session.query(Department).filter_by(name="Engineering").first()
        mkt_dept = db.session.query(Department).filter_by(name="Marketing").first()

        if not (hr_dept and eng_dept and mkt_dept):
            print("Adding dummy departments.")
            if not hr_dept: hr_dept = Department(name="Human Resources")
            if not eng_dept: eng_dept = Department(name="Engineering")
            if not mkt_dept: mkt_dept = Department(name="Marketing")
            db.session.add_all([hr_dept, eng_dept, mkt_dept])
            db.session.commit()
            
            hr_dept = db.session.query(Department).filter_by(name="Human Resources").first()
            eng_dept = db.session.query(Department).filter_by(name="Engineering").first()
            mkt_dept = db.session.query(Department).filter_by(name="Marketing").first()
            print("Dummy Departments added and committed successfully.")
        else:
            print("Departments already exist, skipping dummy department insertion.")


        
        print("Checking for existing Employees and adding more dummy data with specified names...")
        dummy_employees_data = [
            {
                "employeeId": "TEST001", "name": "Fancy Chepngetich", "department": "Testing",
                "profilePic": "https://placehold.co/150x150/FFC0CB/000?text=DU",
                "role": "Tester", "email": "debug.user@example.com", "phone": "555-123-4567",
                "hireDate": date(2024, 1, 1), "currentStatus": "Active"
            },
    
            {
                "employeeId": "EMP002", "name": "Fancy Byegon", "department": "Engineering",
                "profilePic": "https://placehold.co/150x150/CCE0FB/000?text=FB", 
                "role": "Software Engineer", "email": "fancy.b@example.com", "phone": "555-111-2222",
                "hireDate": date(2023, 5, 10), "currentStatus": "Active"
            },
            {
                "employeeId": "EMP003", "name": "Hope Wasonga", "department": "Human Resources",
                "profilePic": "https://placehold.co/150x150/FFDDC1/000?text=HW", 
                "role": "HR Manager", "email": "hope.w@example.com", "phone": "555-333-4444",
                "hireDate": date(2022, 11, 15), "currentStatus": "Active"
            },
            {
                "employeeId": "EMP004", "name": "Carlos Kiplangat", "department": "Marketing",
                "profilePic": "https://placehold.co/150x150/E6FFCC/000?text=CK", 
                "role": "Marketing Specialist", "email": "carlos.k@example.com", "phone": "555-555-6666",
                "hireDate": date(2024, 3, 20), "currentStatus": "Active"
            },
            {
                "employeeId": "EMP005", "name": "David Brown", "department": "Engineering",
                "profilePic": "https://placehold.co/150x150/B8FFF9/000?text=DB",
                "role": "DevOps Engineer", "email": "david.b@example.com", "phone": "555-777-8888",
                "hireDate": date(2023, 8, 1), "currentStatus": "On Leave"
            }
            
        ]

        created_employee_objs = {}

        for emp_data in dummy_employees_data:
            existing_emp = db.session.query(Employee).filter_by(employeeId=emp_data["employeeId"]).first()
            if not existing_emp:
                print(f"Adding employee '{emp_data['employeeId']}' - {emp_data['name']}")
                new_employee = Employee(**emp_data)
                db.session.add(new_employee)
                db.session.commit()
                created_employee_objs[new_employee.employeeId] = new_employee
            else:
                
                print(f"Employee '{emp_data['employeeId']}' already exists, updating name to {emp_data['name']}.")
                existing_emp.name = emp_data['name']
                existing_emp.department = emp_data['department'] 
                existing_emp.profilePic = emp_data['profilePic']
                existing_emp.role = emp_data['role']
                existing_emp.email = emp_data['email']
                existing_emp.phone = emp_data['phone']
                existing_emp.hireDate = emp_data['hireDate']
                existing_emp.currentStatus = emp_data['currentStatus']
                db.session.commit()
                created_employee_objs[existing_emp.employeeId] = existing_emp

        
        print("Checking for existing Attendance Records and adding more...")
        
        today = date.today()
        existing_attendance_ids = {ar.employee.employeeId for ar in db.session.query(AttendanceRecord).filter(AttendanceRecord.date == today).all() if ar.employee}

        attendance_records_to_add = []

        if "TEST001" in created_employee_objs and "TEST001" not in existing_attendance_ids:
            attendance_records_to_add.append(AttendanceRecord(
                employee_id=created_employee_objs["TEST001"].id,
                date=today,
                status="Present",
                check_in_time="09:00",
                check_out_time="17:00"
            ))
        if "EMP002" in created_employee_objs and "EMP002" not in existing_attendance_ids:
            attendance_records_to_add.append(AttendanceRecord(
                employee_id=created_employee_objs["EMP002"].id,
                date=today,
                status="Present",
                check_in_time="08:45",
                check_out_time="17:30"
            ))
        if "EMP003" in created_employee_objs and "EMP003" not in existing_attendance_ids:
            attendance_records_to_add.append(AttendanceRecord(
                employee_id=created_employee_objs["EMP003"].id,
                date=today - timedelta(days=1), 
                status="Present",
                check_in_time="09:15",
                check_out_time="17:00"
            ))
        if "EMP004" in created_employee_objs and "EMP004" not in existing_attendance_ids:
            attendance_records_to_add.append(AttendanceRecord(
                employee_id=created_employee_objs["EMP004"].id,
                date=today,
                status="Absent",
                details="Sick day"
            ))

        if attendance_records_to_add:
            db.session.add_all(attendance_records_to_add)
            db.session.commit()
            print(f"Added {len(attendance_records_to_add)} new Attendance Records.")
        else:
            print("No new Attendance Records to add.")


        
        print("Checking for existing Leave Requests and adding more...")
        existing_leave_requests = db.session.query(LeaveRequest).all()
        
        existing_leave_keys = {(lr.employee_id, lr.start_date, lr.end_date) for lr in existing_leave_requests}

        leave_requests_to_add = []

        
        if "TEST001" in created_employee_objs:
            leave_key = (created_employee_objs["TEST001"].id, date(2024, 7, 1), date(2024, 7, 5))
            if leave_key not in existing_leave_keys:
                leave_requests_to_add.append(LeaveRequest(
                    employee_id=created_employee_objs["TEST001"].id,
                    leave_type="Annual",
                    start_date=date(2024, 7, 1),
                    end_date=date(2024, 7, 5),
                    status="Pending"
                ))
        if "EMP002" in created_employee_objs: 
            leave_key = (created_employee_objs["EMP002"].id, today + timedelta(days=7), today + timedelta(days=7))
            if leave_key not in existing_leave_keys:
                leave_requests_to_add.append(LeaveRequest(
                    employee_id=created_employee_objs["EMP002"].id,
                    leave_type="Sick Leave",
                    start_date=today + timedelta(days=7),
                    end_date=today + timedelta(days=7),
                    status="Approved",
                    reason="Doctor's appointment"
                ))
        if "EMP005" in created_employee_objs: 
            leave_key = (created_employee_objs["EMP005"].id, date(2025, 1, 10), date(2025, 1, 20))
            if leave_key not in existing_leave_keys:
                leave_requests_to_add.append(LeaveRequest(
                    employee_id=created_employee_objs["EMP005"].id,
                    leave_type="Annual Leave",
                    start_date=date(2025, 1, 10),
                    end_date=date(2025, 1, 20),
                    status="Approved",
                    reason="Vacation to Zanzibar"
                ))

        if leave_requests_to_add:
            db.session.add_all(leave_requests_to_add)
            db.session.commit()
            print(f"Added {len(leave_requests_to_add)} new Leave Requests.")
        else:
            print("No new Leave Requests to add.")


    except Exception as e:
        print(f"!!! CRITICAL ERROR during database initialization or dummy data insertion: {e}")
        traceback.print_exc()
    print("--- Database Initialization Attempt Complete ---\n")



api.add_resource(EmployeeListResource, '/employees')
api.add_resource(EmployeeResource, '/employees/<string:employee_id>')
api.add_resource(AttendanceListResource, '/attendance')
api.add_resource(AttendanceResource, '/attendance/<int:attendance_id>')
api.add_resource(LeaveRequestListResource, '/leaves')
api.add_resource(LeaveRequestResource, '/leaves/<int:leave_id>')
api.add_resource(DepartmentListResource, '/departments')


if __name__ == '__main__':
    app.run(debug=True, port=3000)