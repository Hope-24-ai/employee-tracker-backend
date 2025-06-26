from flask import Blueprint, jsonify

bp = Blueprint('dashboard_routes', __name__, url_prefix='/dashboard')

@bp.route('/', methods=['GET'])
def dashboard_data():
    return jsonify({"message": "Dashboard route ready"})
