from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    activities = db.relationship('ActivityData', backref='user', lazy=True)

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
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    exercise_type_id = db.Column(db.Integer, db.ForeignKey('exercise_types.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # Store as YYYY-MM-DD
    duration_minutes = db.Column(db.Integer, nullable=False)
    calories_burnt = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<ActivityData {self.id} - {self.date}>'

class SharedContent(db.Model):
    __tablename__ = 'shared_content'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    shared_with_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'activity', 'achievement', 'stats'
    content_id = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    share_date = db.Column(db.String(10), nullable=False)  # Store as YYYY-MM-DD
    
    def __repr__(self):
        return f'<SharedContent {self.id} - {self.content_type}>'