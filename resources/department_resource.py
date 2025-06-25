from flask_restful import Resource
from flask import request
from models import db, Department

class DepartmentListResource(Resource):
    def get(self):
        departments = Department.query.all()
        return [{"id": d.id, "name": d.name} for d in departments], 200

    def post(self):
        data = request.get_json()
        department = Department(name=data["name"])
        db.session.add(department)
        db.session.commit()
        return {"message": "Department added"}, 201
