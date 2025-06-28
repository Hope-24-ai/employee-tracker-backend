from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Employee, PerformanceReview
from datetime import datetime

# Helper function to get the current logged in user
def current_user():
    return Employee.query.get(get_jwt_identity())


class ReviewListResource(Resource):
    @jwt_required()
    def get(self):
        user = current_user()
        # If user is a manager fetch all reviews for employees in their department
        if user.user_type_name == "Manager":
            reviews = PerformanceReview.query.join(Employee).filter(
                Employee.department_id == user.department_id
            ).all()
        # Otherwise--> show only the reviews of the employee themselves
        else:
            reviews = PerformanceReview.query.filter_by(employee_id=user.id).all()

        return make_response([r.to_dict() for r in reviews], 200)
    
    @jwt_required()
    def post(self):
        user = current_user()
        # Only managers can add new reviews
        if user.user_type_name != "Manager":
            return make_response({"error": "Only managers can add reviews"}, 403)
            
        # Create a new review for an employee
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


class ReviewDetailResource(Resource):
    @jwt_required()
    def put(self, id):
        user = current_user()
        review = PerformanceReview.query.get_or_404(id)

        # Only manager of same department can edit
        if user.user_type_name != "Manager" or review.employee.department_id != user.department_id:
            return make_response({"error": "Forbidden"}, 403)
        # Update editable fields --->notes and rating<---
        data = request.get_json()
        for field in ["notes", "rating"]:
            if field in data:
                setattr(review, field, data[field])
        db.session.commit()
        return make_response(review.to_dict(), 200)
    
    @jwt_required()
    def delete(self, id):
        user = current_user()
        review = PerformanceReview.query.get_or_404(id)
        # Managers can only delete reviews within their own department
        if user.user_type_name != "Manager" or review.employee.department_id != user.department_id:
            return make_response({"error": "Forbidden"}, 403)

        db.session.delete(review)
        db.session.commit()
        return {}, 204
