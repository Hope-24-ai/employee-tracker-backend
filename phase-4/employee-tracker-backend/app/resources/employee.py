from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Employee, UserType, JobTitle, db

#  Get the current logged in user
def current_user():
    return Employee.query.get(get_jwt_identity())


# ==== EMPLOYEE LIST------------------------------- 
class EmployeeListResource(Resource):
    @jwt_required()
    def get(self):
        user = current_user()

        # HR can view all employees
        if user.user_type_name == "HR":
            employees = Employee.query.all()
        # Managers can view employees in their department
        elif user.user_type_name == "Manager":
            employees = Employee.query.filter_by(department_id=user.department_id).all()
        else:
            return make_response({"error": "Forbidden"}, 403)

        return make_response([e.to_dict() for e in employees], 200)

    @jwt_required()
    def post(self):
        user = current_user()

        # Only HR can create employees
        if user.user_type_name != "HR":
            return make_response({"error": "Only HR can create employees"}, 403)

        data = request.get_json()
        required_fields = ["first_name", "last_name", "email", "password", "user_type_name", "job_title_name", "department_id"]
        missing = [field for field in required_fields if field not in data]
        if missing:
            return make_response({"error": f"Missing fields: {', '.join(missing)}"}, 400)

        if Employee.query.filter_by(email=data["email"].strip().lower()).first():
            return make_response({"error": "Email already exists"}, 400)

        user_type = UserType.query.filter_by(name=data["user_type_name"]).first()
        if not user_type:
            return make_response({"error": "Invalid user type"}, 400)

        job_title = JobTitle.query.filter_by(title=data["job_title_name"]).first()
        if not job_title:
            return make_response({"error": "Invalid job title"}, 400)

        new_employee = Employee(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"].strip().lower(),
            phone=data.get("phone"),
            department_id=data["department_id"],
            user_type_id=user_type.id,
            job_title_id=job_title.id
        )
        new_employee.set_password(data["password"])

        try:
            db.session.add(new_employee)
            db.session.commit()
            return make_response(new_employee.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({"error": str(e)}, 500)


#  EMPLOYEE DETAIL 
class EmployeeDetailResource(Resource):
    @jwt_required()
    def get(self, id):
        user = current_user()

        target_employee = Employee.query.get(id)
        if not target_employee:
            return make_response({"error": "Employee not found"}, 404)

        # HR can view anyone, managers their department, and users themselves
        if (
            user.user_type_name == "HR"
            or (user.user_type_name == "Manager" and user.department_id == target_employee.department_id)
            or user.id == id
        ):
            return make_response(target_employee.to_dict(), 200)

        return make_response({"error": "Forbidden"}, 403)
