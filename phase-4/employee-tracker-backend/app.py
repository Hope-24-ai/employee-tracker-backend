

from flask import Flask
from flask_cors import CORS
from app.models import db
from login import login_bp

app = Flask(__name__)
app.secret_key = "super-secret"  # Replace with a secure key in production

# ✅ Allow the React frontend origin and enable credentials (e.g. session cookies)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(login_bp)
