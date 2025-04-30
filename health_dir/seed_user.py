# seed_user.py

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Create a new user
    new_user = User(
        username='testuser',
        email='testuser@example.com'
    )
    new_user.set_password('Test@1234')  # Set a meaningful password

    db.session.add(new_user)
    db.session.commit()

    print('New user added successfully!')
