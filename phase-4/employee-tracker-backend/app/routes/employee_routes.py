from flask import Blueprint, jsonify

bp = Blueprint('employee_routes', __name__, url_prefix='/employees')

@bp.route('/', methods=['GET'])
def get_employees():
    return jsonify({"message": "Employee route ready"})
