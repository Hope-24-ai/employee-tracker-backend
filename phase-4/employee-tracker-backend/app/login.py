# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.models import db, Employee, Admin



app = Flask(__name__)
app.secret_key = "super-secret"

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username')
    password = data.get('password')

    if not password:
        return jsonify({"error": "Password is required"}), 400

    if password == "adminpass":
        admin = Admin.query.first()
        if admin:
            return jsonify({
                "message": "Logged in as admin",
                "role": "admin",
                "admin": {"id": admin.id, "name": admin.name}
            })
        else:
            return jsonify({"error": "No admin found"}), 404

    employee = Employee.query.filter_by(username=username_or_email, password=password).first()
    if employee:
        return jsonify({
            "message": "Logged in as employee",
            "role": "employee",
            "employee": {"id": employee.id, "name": employee.name}
        })

    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


