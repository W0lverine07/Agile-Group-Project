from flask import Flask
from flask_migrate import Migrate
from app.models import db
import os
from .db_init import populate_exercise_types

def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

    app.secret_key = 'secretkey104'
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, '..', 'instance', 'wellness.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    
    
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        populate_exercise_types()  # Populate exercise types table
    Migrate(app, db)
    
    from app.routes import main
    app.register_blueprint(main)

    return app

