from app import create_app
from app.models import db
from app.db_init import populate_exercise_types

app = create_app()

with app.app_context():
    try:
        # This will create all tables if they don't exist
        db.create_all()
        
        # Now populate the tables
        populate_exercise_types()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        db.session.rollback()