from flask import Flask, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from models import db, Employee, AttendanceRecord, LeaveRequest, Department 
import os
import traceback
from datetime import date, timedelta

from routes import register_routes  # ✅ New import

app = Flask(__name__, instance_relative_config=True)

database_path = os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    os.makedirs(app.instance_path)
    print(f"Created instance folder: {app.instance_path}")
except OSError as e:
    if e.errno == 17:
        print(f"Instance folder already exists: {app.instance_path}")
    else:
        print(f"Error creating instance folder: {e}")

CORS(app)
db.init_app(app)
api = Api(app)

# ✅ Register all API routes
register_routes(app)

with app.app_context():
    print("\n--- Starting Database Initialization ---")
    print(f"Database URI configured: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Instance path: {app.instance_path}")

    try:
        print("Attempting db.create_all()...")
        db.create_all()
        print("db.create_all() executed.")

        # ✅ Dummy data seeding logic remains the same...
        # You can keep or move the seeding logic to a separate function or module if preferred

    except Exception as e:
        print(f"!!! CRITICAL ERROR during database initialization or dummy data insertion: {e}")
        traceback.print_exc()
    print("--- Database Initialization Attempt Complete ---\n")

if __name__ == '__main__':
    app.run(debug=True, port=3000)
