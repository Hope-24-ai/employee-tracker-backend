import re
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

# Metadata for naming conventions
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

# --- Admin Model ---
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

# deparmt
class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(225))

    employees = db.relationship('Employee', back_populates='department', cascade='all, delete-orphan')
    serialize_rules = ("-employees.department",)

# ___________--------_____
# user type
# ___________________
class UserType(db.Model, SerializerMixin):
    __tablename__ = 'user_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(225))

    employees = db.relationship('Employee', back_populates='user_type')
    serialize_rules = ("-employees.user_type",)
    
# _______________------_____________
# ---------------j0b tittle---------->
class JobTitle(db.Model, SerializerMixin):
    __tablename__ = 'job_titles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)

    employees = db.relationship('Employee', back_populates='job_title')
    serialize_rules = ("-employees.job_title",)

# --- Employee Model ---
class Employee(db.Model,SerializerMixin):
    __tablename__ = 'employees'

    serialize_rules = (
        "-department.employees",
        "-role.employees",
        "-attendances.employee",
        "-reviews.employee",
        "-password_hash",
        "-user_type.employees",
        "-job_title.employees",
    )
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    phone = db.Column(db.String(100))
    hire_date = db.Column(db.DateTime, default=datetime.now)

    password_hash = db.Column(db.String(128), nullable=False)

    # FK
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_types.id'))
    job_title_id = db.Column(db.Integer, db.ForeignKey('job_titles.id'))
# RLNSHP
    department = db.relationship('Department', back_populates='employees')
    user_type = db.relationship('UserType', back_populates='employees')
    job_title = db.relationship('JobTitle', back_populates='employees')
    # Relationship
    leave_applications = db.relationship('LeaveApplication', back_populates='employee', cascade="all, delete-orphan")
    reviews = db.relationship('PerformanceReview', back_populates='employee', cascade='all, delete-orphan')
    attendances = db.relationship('Attendance', back_populates='employee', cascade='all, delete-orphan')
  # association
    department_name = association_proxy('department', 'name')
    user_type_name = association_proxy('user_type', 'name')
    job_title_name = association_proxy('job_title', 'title')

    def set_password(self, raw_password):
        from flask_bcrypt import generate_password_hash
        self.password_hash = generate_password_hash(raw_password).decode('utf-8')

    def verify_password(self, raw_password):
        from flask_bcrypt import check_password_hash
        return check_password_hash(self.password_hash, raw_password)

    @validates("email")
    def validate_email(self, key, value):
        normalized = value.strip().lower()
        regex = r"[A-Za-z][A-Za-z0-9_.]*@[A-Za-z0-9]+\.[a-z]{2,}"
        if not re.match(regex, normalized):
            raise ValueError("Invalid email format")
        return normalized

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