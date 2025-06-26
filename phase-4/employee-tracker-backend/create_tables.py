from app import create_app, db
from app.models import Admin, Employee  # ✅ Import your models here
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")

    # Seed admin
    if not Admin.query.first():
        admin = Admin(
            name="Admin User",
            email="admin@example.com",
            password=generate_password_hash("adminpass")
        )
        db.session.add(admin)
        print("Admin created: admin@example.com / adminpass")

    # Seed employee
    if not Employee.query.first():
        employee = Employee(
            name="Employee One",
            email="employee@example.com",
            password=generate_password_hash("123456")
        )
        db.session.add(employee)
        print("👤 Employee created: employee@example.com / 123456")

    db.session.commit()
    print("✅ Default users added.")

