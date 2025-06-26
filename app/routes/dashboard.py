from flask import Blueprint, jsonify, request
from app.models.metric import DashboardMetric
from app.db import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# ✅ Home test route
@dashboard_bp.route('/')
def dashboard_home():
    return jsonify(message="Welcome to the dashboard")

# 📊 Get all metrics
@dashboard_bp.route('/metrics')
def get_metrics():
    metrics = DashboardMetric.query.all()
    return jsonify([{'id': m.id, 'name': m.name, 'value': m.value} for m in metrics])

# ➕ Create a new metric
@dashboard_bp.route('/metrics', methods=['POST'])
def create_metric():
    data = request.get_json()
    name = data.get('name')
    value = data.get('value')

    if not name or value is None:
        return jsonify(error="Missing 'name' or 'value'"), 400

    new_metric = DashboardMetric(name=name, value=value)
    db.session.add(new_metric)
    db.session.commit()

    return jsonify(message="Metric created", id=new_metric.id), 201

# 🔄 Update a metric
@dashboard_bp.route('/metrics/<int:id>', methods=['PATCH'])
def update_metric(id):
    metric = DashboardMetric.query.get_or_404(id)
    data = request.get_json()

    metric.name = data.get('name', metric.name)
    metric.value = data.get('value', metric.value)

    db.session.commit()
    return jsonify(message="Metric updated")

# ❌ Delete a metric
@dashboard_bp.route('/metrics/<int:id>', methods=['DELETE'])
def delete_metric(id):
    metric = DashboardMetric.query.get_or_404(id)
    db.session.delete(metric)
    db.session.commit()
    return jsonify(message="Metric deleted")
