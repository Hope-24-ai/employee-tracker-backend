from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Employee, PerformanceReview
from datetime import datetime