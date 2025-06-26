from app import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    # TODO: Add fields like employee_id, content, rating
