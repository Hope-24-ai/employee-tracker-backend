# app.py
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from config import Config
from models import db

# Import all resource classes
from resources.employee_resource import EmployeeListResource
from resources.leave_request_resource import LeaveRequestListResource, LeaveRequestResource
from resources.attendance_resource import AttendanceListResource, AttendanceResource
from resources.department_resource import DepartmentListResource  # Optional if you added Department model

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
api = Api(app)
db.init_app(app)

# Routes
api.add_resource(EmployeeListResource, '/employees')

api.add_resource(LeaveRequestListResource, '/leaves')
api.add_resource(LeaveRequestResource, '/leaves/<int:leave_id>')

api.add_resource(AttendanceListResource, '/attendance')
api.add_resource(AttendanceResource, '/attendance/<int:attendance_id>')

# Optional if you have a Department model and resource
api.add_resource(DepartmentListResource, '/departments')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates tables if not exist
    app.run(debug=True, port=3000)
