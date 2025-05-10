from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

# Define the models for the application
# Making username as the primary key for the User table and user_details table
class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(50), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship to user details (one-to-one)
    details = db.relationship('UserDetails', backref='user', uselist=False, cascade="all, delete-orphan")
    activities = db.relationship('ActivityData', backref='user', lazy=True)

class UserDetails(db.Model):
    __tablename__ = 'user_details'
    username = db.Column(db.String(50), db.ForeignKey('user.username'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    dob = db.Column(db.Date, nullable=False) # Date of Birth
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)

class ExerciseType(db.Model):
    __tablename__ = 'exercise_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    calories_per_minute = db.Column(db.Float, nullable=False)
    
    activities = db.relationship('ActivityData', backref='exercise_type', lazy=True)
    
    def __repr__(self):
        return f'<ExerciseType {self.name}>'

class ActivityData(db.Model):
    __tablename__ = 'activity_data'
    
    id = db.Column(db.String(50), primary_key=True)  # Changed to String/VARCHAR
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    exercise_type_id = db.Column(db.Integer, db.ForeignKey('exercise_types.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    calories_burnt = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<ActivityData {self.id} - {self.date}>'

# Updateed the SharedContent model to use username instead of user_id
class SharedContent(db.Model):
    __tablename__ = 'shared_content'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)  # Changed
    shared_with_username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)  # Changed
    content_type = db.Column(db.String(20), nullable=False)
    content_id = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    share_date = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<SharedContent {self.id} - {self.content_type}>'
