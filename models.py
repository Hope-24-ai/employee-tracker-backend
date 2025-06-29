from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import date

db = SQLAlchemy()


class BaseMixin(SerializerMixin):
    pass


class Employee(db.Model, BaseMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    employeeId = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    profilePic = db.Column(db.String(255), default='https://placehold.co/150x150/FFF/000?text=JP')
    role = db.Column(db.String(100), nullable=False, default='Employee')  # Updated: enforce default role
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    hireDate = db.Column(db.Date, default=date.today)
    currentStatus = db.Column(db.String(50), default='Active')

    attendance_records = db.relationship('AttendanceRecord', backref='employee', lazy=True)
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employeeId': self.employeeId,
            'name': self.name,
            'department': self.department,
            'profilePic': self.profilePic,
            'role': self.role,
            'email': self.email,
            'phone': self.phone,
            'hireDate': self.hireDate.isoformat() if isinstance(self.hireDate, date) else None,
            'currentStatus': self.currentStatus
        }


class AttendanceRecord(db.Model, BaseMixin):
    __tablename__ = 'attendance_records'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    check_in_time = db.Column(db.String(50))
    check_out_time = db.Column(db.String(50))
    details = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.isoformat() if isinstance(self.date, date) else None,
            'status': self.status,
            'check_in_time': self.check_in_time,
            'check_out_time': self.check_out_time,
            'details': self.details
        }


class LeaveRequest(db.Model, BaseMixin):
    __tablename__ = 'leave_requests'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    reason = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'leave_type': self.leave_type,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, date) else None,
            'end_date': self.end_date.isoformat() if isinstance(self.end_date, date) else None,
            'status': self.status,
            'reason': self.reason
        }


class Department(db.Model, BaseMixin):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
