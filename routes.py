# routes.py

from flask_restful import Api

from resources.employee_resource import EmployeeListResource, EmployeeResource
from resources.attendance_resource import AttendanceListResource, AttendanceResource
from resources.leave_request_resource import LeaveRequestListResource, LeaveRequestResource
from resources.department_resource import DepartmentListResource

def register_routes(app):
    api = Api(app)

    # Employee Routes
    api.add_resource(EmployeeListResource, '/employees')
    api.add_resource(EmployeeResource, '/employees/<string:employee_id>')

    # Attendance Routes
    api.add_resource(AttendanceListResource, '/attendance')
    api.add_resource(AttendanceResource, '/attendance/<int:attendance_id>')

    # Leave Request Routes
    api.add_resource(LeaveRequestListResource, '/leaves')
    api.add_resource(LeaveRequestResource, '/leaves/<int:leave_id>')

    # Department Routes
    api.add_resource(DepartmentListResource, '/departments')
