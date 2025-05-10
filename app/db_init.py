from app.models import db, ExerciseType
from sqlalchemy import inspect

def populate_exercise_types():
    """Populate the exercise_types table with initial data"""
    try:
        # Check if table exists
        inspector = inspect(db.engine)
        if 'exercise_types' not in inspector.get_table_names():
            db.create_all()
            print("Created exercise_types table")

        # Define the default exercise types
        exercise_types = [
            {'id': 1, 'name': 'Running', 'calories_per_minute': 11.5},
            {'id': 2, 'name': 'Walking', 'calories_per_minute': 5.0},
            {'id': 3, 'name': 'Cycling', 'calories_per_minute': 8.5},
            {'id': 4, 'name': 'Swimming', 'calories_per_minute': 10.0},
            {'id': 5, 'name': 'Hiking', 'calories_per_minute': 7.0},
            {'id': 6, 'name': 'Weight Training', 'calories_per_minute': 6.0},
            {'id': 7, 'name': 'Yoga', 'calories_per_minute': 3.5},
            {'id': 8, 'name': 'Dancing', 'calories_per_minute': 7.5},
            {'id': 9, 'name': 'Basketball', 'calories_per_minute': 9.0},
            {'id': 10, 'name': 'Soccer', 'calories_per_minute': 10.0}
        ]
        
        # Track if we added any new exercises
        added_count = 0
        
        for exercise_data in exercise_types:
            existing = db.session.get(ExerciseType, exercise_data['id'])
            if not existing:
                exercise_type = ExerciseType(
                    id=exercise_data['id'],
                    name=exercise_data['name'],
                    calories_per_minute=exercise_data['calories_per_minute']
                )
                db.session.add(exercise_type)
                added_count += 1
        
        db.session.commit()
        print(f"Exercise types population complete. Added {added_count} new exercises.")
        
    except Exception as e:
        print(f"Error in populate_exercise_types: {e}")
        db.session.rollback()
        raise