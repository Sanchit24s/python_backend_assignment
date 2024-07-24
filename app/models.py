from app import db
from datetime import datetime

class Retreat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    user_phone = db.Column(db.String(20), nullable=False)
    retreat_id = db.Column(db.Integer, db.ForeignKey('retreat.id'), nullable=False)
    retreat_title = db.Column(db.String(100), nullable=False)
    retreat_location = db.Column(db.String(100), nullable=False)
    retreat_price = db.Column(db.Float, nullable=False)
    retreat_duration = db.Column(db.Integer, nullable=False)
    payment_details = db.Column(db.String(200), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    retreat = db.relationship('Retreat', backref=db.backref('bookings', lazy=True))