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
    @jwt_required()
    def post(self):
        user = current_user()
        if user.role_name != "Manager":
            return make_response({"error": "Only managers can add reviews"}, 403)

        data = request.get_json()
        review = PerformanceReview(
            employee_id=data["employee_id"],
            reviewer=f"{user.first_name} {user.last_name}",
            notes=data.get("notes"),
            rating=data.get("rating"),
            review_date=datetime.now().date(),
        )
        db.session.add(review)
        db.session.commit()
        return make_response(review.to_dict(), 201)
