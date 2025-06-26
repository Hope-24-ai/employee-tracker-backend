# models.py

from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# --- Admin Model ---
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

# --- Employee Model ---
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship
    leave_applications = db.relationship('LeaveApplication', back_populates='employee', cascade="all, delete-orphan")

# --- LeaveApplication Model ---
class LeaveApplication(db.Model):
    __tablename__ = 'leave_applications'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    reason = db.Column(db.String)
    status = db.Column(db.String, default='Pending')

    # Relationship
    employee = db.relationship('Employee', back_populates='leave_applications')


class PerformanceReview(db.Model, SerializerMixin):
    __tablename__ = 'performance_reviews'

    id = db.Column(db.Integer, primary_key=True)
    review_date = db.Column(db.DateTime, default=datetime.now)
    reviewer = db.Column(db.String(50))
    notes = db.Column(db.Text)
    rating = db.Column(db.Integer)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    employee = db.relationship('Employee', back_populates='reviews')

    serialize_rules = ("-employee.reviews",)