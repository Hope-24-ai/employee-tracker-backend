# seed.py
from app import create_app
from models import db, Employee
from datetime import date

app = create_app()

with app.app_context():
    print("\n--- Seeding Database ---")

    db.drop_all()
    db.create_all()

    employees = [
        Employee(
            employeeId='EMP004',
            name='Carlos Kiplangat',
            role='Marketing Specialist',
            department='Marketing',
            email='carlos.kiplangat@company.com',
            phone='0701234567',
            hireDate=date(2022, 6, 1),
            currentStatus='Active'
        ),
        Employee(
            employeeId='EMP005',
            name='David Brown',
            role='DevOps Engineer',
            department='Engineering',
            email='david.brown@company.com',
            phone='0709876543',
            hireDate=date(2023, 1, 15),
            currentStatus='On Leave'
        ),
        Employee(
            employeeId='EMP002',
            name='Fancy Byegon',
            role='Software Engineer',
            department='Engineering',
            email='fancy.byegon@company.com',
            phone='0711122233',
            hireDate=date(2023, 3, 1),
            currentStatus='Active'
        ),
        Employee(
            employeeId='TEST001',
            name='Fancy Chepngetich',
            role='Tester',
            department='Testing',
            email='fancy.chepngetich@company.com',
            phone='0712345678',
            hireDate=date(2024, 1, 5),
            currentStatus='Active'
        ),
        Employee(
            employeeId='EMP003',
            name='Hope Wasonga',
            role='HR Manager',
            department='Human Resources',
            email='hope.w@example.com',
            phone='555-333-4444',
            hireDate=date(2022, 11, 15),
            currentStatus='Active'
        ),
    ]

    db.session.bulk_save_objects(employees)
    db.session.commit()

    print("✅ Employee data seeded successfully.\n")
