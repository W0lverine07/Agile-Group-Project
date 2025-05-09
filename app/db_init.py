from app.models import db, ExerciseType

def populate_exercise_types():
    """Populate the exercise_types table with initial data"""
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
    
    # Add exercise types if they don't exist
    for exercise_data in exercise_types:
        existing = ExerciseType.query.get(exercise_data['id'])
        if not existing:
            exercise_type = ExerciseType(
                id=exercise_data['id'],
                name=exercise_data['name'],
                calories_per_minute=exercise_data['calories_per_minute']
            )
            db.session.add(exercise_type)
    
    db.session.commit()
    print("Exercise types have been populated.")