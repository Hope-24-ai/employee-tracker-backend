from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.String)
    position = db.Column(db.String, nullable=False)
    salary = db.Column(db.Float, nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError("Name must be at least 3 characters long.")
        return name

    @validates('salary')
    def validate_salary(self, key, salary):
        if salary is not None and salary < 0:
            raise ValueError("Salary must be positive.")
        return salary
