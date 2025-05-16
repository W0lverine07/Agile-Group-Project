from flask import Flask
from flask_migrate import Migrate
from app.models import db
import os
from .db_init import populate_exercise_types
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

    app.secret_key = 'secretkey104'
    csrf = CSRFProtect(app) #Enables CSRF protection
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, '..', 'instance', 'wellness.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initializing database within app context
    with app.app_context():
        db.create_all()
        try:
            populate_exercise_types()
        except Exception as e:
            print(f"Error populating exercise types: {e}")
    
    from app.routes import main
    app.register_blueprint(main)

    return app

