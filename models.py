# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employeeId = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))

class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employeeId = db.Column(db.String(20), db.ForeignKey('employee.employeeId'))
    date = db.Column(db.String(50))
    status = db.Column(db.String(20))

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employeeId = db.Column(db.String(20), db.ForeignKey('employee.employeeId'))
    type = db.Column(db.String(50))
    startDate = db.Column(db.String(50))
    endDate = db.Column(db.String(50))
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
