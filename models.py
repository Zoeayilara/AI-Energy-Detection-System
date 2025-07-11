from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(200))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Facility(db.Model):
    __tablename__ = 'facility'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Float, nullable=False)  # in kW
    solar_panels = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    energy_records = db.relationship('EnergyData', back_populates='facility', lazy='dynamic')


class EnergyData(db.Model):
    __tablename__ = 'energy_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    energy_produced = db.Column(db.Float, nullable=False)
    energy_consumed = db.Column(db.Float, nullable=False)
    efficiency = db.Column(db.Float, nullable=False)
    current_load = db.Column(db.Float, nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    
    # Electrical parameters for voltage monitoring
    voltage = db.Column(db.Float, nullable=True)
    current = db.Column(db.Float, nullable=True)
    frequency = db.Column(db.Float, nullable=True)
    power_factor = db.Column(db.Float, nullable=True)
    
    # Alert data
    alert_message = db.Column(db.String(255), nullable=True)
    alert_level = db.Column(db.String(50), nullable=True)  # "info", "warning", "critical"
    
    facility = db.relationship('Facility', back_populates='energy_records')