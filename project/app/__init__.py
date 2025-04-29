from flask import Flask
import os

def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

    app.secret_key = 'secretkey104'
    
    from app.routes import main
    app.register_blueprint(main)

    return app

