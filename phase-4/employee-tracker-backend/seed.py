# seed.py
from app import create_app, db
from app.models import Employee
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Using DB:", app.config["SQLALCHEMY_DATABASE_URI"])

    db.create_all()

    hashed_pw = generate_password_hash("password123")
    e1 = Employee(name="Hope Yunia", email="hope@example.com", password_hash=hashed_pw)

    db.session.add(e1)
    db.session.commit()
    print("Seed complete.")


