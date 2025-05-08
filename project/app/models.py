from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    dob = db.Column(db.Date, nullable=False) # Date of Birth
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)