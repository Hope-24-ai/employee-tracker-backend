from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from .models import db


app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init extensions
db.init_app(app)
migrate = Migrate(app, db)

# API setup
api = Api(app)


@app.route("/")
def home():
    return "🎉 Flask backend is working!"

if __name__ == "__main__":
    app.run(debug=True)

