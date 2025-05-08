from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.db_helper import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from datetime import datetime
from app.models import db, UserDetails, User
from flask import jsonify
import random

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')  

# Generate a unique user ID for the new user
def generate_unique_user_id():
    while True:
        user_id = random.randint(100000, 999999)
        if not User.query.filter_by(user_id=user_id).first():
            return user_id

@main.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not username or not password or not confirm_password:
        flash("All fields are required", "error")
        return redirect(url_for('main.home'))

    if password != confirm_password:
        flash("Passwords do not match", "error")
        return redirect(url_for('main.home'))

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("Username already exists", "error")
        return redirect(url_for('main.home'))

    hashed_pw = generate_password_hash(password)
    user_id = generate_unique_user_id()
    new_user = User(user_id=user_id, username=username, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    session['registered_username'] = username  # storing username in session
    return redirect(url_for('main.edit_profile'))

@main.route('/check_username', methods=['POST'])
def check_username():
    username = request.form.get('username')
    exists = User.query.filter_by(username=username).first() is not None
    return jsonify({'exists': exists})

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            flash("Login successful!", "success")
            return redirect(url_for('main.account'))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('main.home'))

    # If GET request, render the login page
    return render_template('login.html')

@main.route('/edit_profile')
def edit_profile():
    username = session.get('registered_username')
    if not username:
        flash("No registration session found. Please register again.", "error")
        return redirect(url_for('main.home'))
    return render_template('edit_profile.html', username=username)

@main.route('/save_profile', methods=['POST'])
def save_profile():
    username = session.get('registered_username')
    if not username:
        flash("Session expired. Please register again.", "error")
        return redirect(url_for('main.home'))

    # get data from form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    blood_group = request.form.get('blood_group')
    dob_str = request.form.get('dob')
    weight = request.form.get('weight')
    height = request.form.get('height')

    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

        user_details = UserDetails(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            blood_group=blood_group,
            dob=dob,
            weight=float(weight),
            height=float(height)
        )

        db.session.add(user_details)
        db.session.commit()
        session.pop('registered_username', None)

        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.account'))
    except Exception as e:
        flash(f"Error saving profile: {e}", "error")
        return redirect(url_for('main.edit_profile'))

@main.route('/account')
def account():
    return render_template('account.html')

@main.route('/upload')
def upload():
    return render_template('upload.html')

@main.route('/visualize')
def visualize():
    return render_template('visualize.html')

@main.route('/share_page')
def share_page():
    return render_template('share_page.html')

@main.route('/health_data', methods=['POST'])
def health_data():
    return render_template('health_data.html')

@main.route('/faqs')
def faqs():
    return render_template('faqs.html')
  
@main.route('/history')
def history():
    return render_template('history.html')

