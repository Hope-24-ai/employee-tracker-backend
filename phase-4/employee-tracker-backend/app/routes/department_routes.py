from flask import Blueprint, jsonify

bp = Blueprint('department_routes', __name__, url_prefix='/departments')

@bp.route('/', methods=['GET'])
def get_departments():
    return jsonify({"message": "Department route ready"})
