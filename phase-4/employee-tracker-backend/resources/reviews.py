from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Employee, PerformanceReview
from datetime import datetime


def current_user():
    return Employee.query.get(get_jwt_identity())


class ReviewListResource(Resource):
    @jwt_required()
    def get(self):
        user = current_user()
        if user.role_name == "Manager":
            reviews = PerformanceReview.query.join(Employee).filter(
                Employee.department_id == user.department_id
            ).all()
        else:
            reviews = PerformanceReview.query.filter_by(employee_id=user.id).all()

        return make_response([r.to_dict() for r in reviews], 200)
