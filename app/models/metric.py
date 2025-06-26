from app.db import db

class DashboardMetric(db.Model):
    __tablename__ = 'dashboard_metrics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Integer, nullable=False)
