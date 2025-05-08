from flask import Flask
from flask_migrate import Migrate
from app.models import db
import os


def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

    app.secret_key = 'secretkey104'
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, '..', 'instance', 'wellness.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    
    db.init_app(app)
    Migrate(app, db)
    
    from app.routes import main
    app.register_blueprint(main)

    return app

