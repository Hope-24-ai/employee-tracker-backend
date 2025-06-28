import os
from datetime import timedelta
from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from models import db

# import and register resources
from resources.auth import AuthResource


# Load environment variables 
load_dotenv()

# Initialize Flask App 
app = Flask(__name__)

# Configurations 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI") 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

 

#  Extensions Initialization 
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)
api = Api(app)

# routes
api.add_resource(AuthResource, '/auth/<string:action>') 






# Entry Point 
if __name__ == "__main__":
    app.run(port=5555, debug=True)