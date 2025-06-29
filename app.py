from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes import register_routes  # Ensure this file exists and defines your Flask routes
import os
import traceback

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # --- Config ---
    database_path = os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Use env var in production

    # --- Ensure instance folder exists ---
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"Instance folder ready: {app.instance_path}")
    except Exception as e:
        print(f"Error ensuring instance folder: {e}")

    # --- Init Extensions ---
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)
    api = Api(app)

    # --- Register Routes ---
    register_routes(app)

    return app

# --- Run Server (for dev) ---
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        print("\n--- Starting Database Initialization ---")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        try:
            db.create_all()
            print("✅ Database initialized.")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            traceback.print_exc()
        print("--- Done ---\n")

    app.run(debug=True, port=5000)
