from flask import Blueprint, jsonify

bp = Blueprint('review_routes', __name__, url_prefix='/reviews')

@bp.route('/', methods=['GET'])
def get_reviews():
    return jsonify({"message": "Review route ready"})
