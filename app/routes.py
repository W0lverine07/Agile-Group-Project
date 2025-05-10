from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.db_helper import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from datetime import datetime, timedelta
from app.models import db, UserDetails, User
from flask import jsonify
from app.models import db, User, ExerciseType, ActivityData, SharedContent
from functools import wraps
import random # for generating random strings (Activity_id)
import string # for generating random strings (Activity_id)
import random, json

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    return render_template('health_data.html')
        
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
    new_user = User(username=username, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    session['registered_username'] = username  #Storing the username in session for later use
    return redirect(url_for('main.edit_profile'))

#start of the check username in database
@main.route('/check_username', methods=['POST'])
def check_username():
    username = request.form.get('username')
    exists = User.query.filter_by(username=username).first() is not None
    return jsonify({'exists': exists})

@main.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session['username'] = username  # Only store username in session not user_id
        session['logged_in'] = True
        flash("Login successful!", "success")
        return redirect(url_for('main.health_data'))
    else:
        flash("Invalid username or password", "error")
        return redirect(url_for('main.home'))

@main.route('/logout')
def logout():
    session.clear()  # Clears all session data
    flash("You have been logged out.", "info")
    return redirect(url_for('main.home'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

#start of the profile page logic
#For edit profile and save profile
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

    # Get data from the form
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

        session.pop('registered_username', None)
        flash("Profile updated successfully! Please log in using your new credentials.", "info")
        return redirect(url_for('main.home'))
    except Exception as e:
        flash(f"Error saving profile: {e}", "error")
        return redirect(url_for('main.edit_profile'))
#end of the profile page logic

@main.route('/account')
@login_required
def account():
    username = session['username']
    user = UserDetails.query.filter_by(username=username).first()

    if not user:
        flash("User profile not found.", "error")
        return redirect(url_for('main.home'))

    return render_template('account.html', user=user)


# Protecting routes that need authentication by adding @login_required
@main.route('/upload')
@login_required
def upload():
    exercise_types = ExerciseType.query.order_by(ExerciseType.name).all()
    return render_template('upload.html', 
                         exercise_types=exercise_types, 
                         today=datetime.now().strftime('%Y-%m-%d'),
                         username=session['username'])

#generating Activity ID in format: username-XXX where XXX is random alphanumeric
def generate_activity_id(username):
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    return f"{username}-{random_chars}"

# Update upload_data route to use username
@main.route('/upload_data', methods=['POST'])
@login_required
def upload_data():
    username = session['username']  # Get username from session
    exercise_type_id = request.form.get('exercise_type', type=int)
    duration = request.form.get('duration', type=int)
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    if not exercise_type_id or not duration:
        flash("Exercise type and duration are required", "error")
        return redirect(url_for('main.upload'))
    
    exercise_type = ExerciseType.query.get(exercise_type_id)
    calories = round(exercise_type.calories_per_minute * duration)
    
    # Generate unique ID
    max_attempts = 5
    for _ in range(max_attempts):
        activity_id = generate_activity_id(username)
        if not ActivityData.query.get(activity_id):
            break
    else:
        flash("Failed to generate unique activity ID. Please try again.", "error")
        return redirect(url_for('main.upload'))
    
    new_activity = ActivityData(
        id=activity_id,
        username=username,  # Now using username instead of user_id
        exercise_type_id=exercise_type_id,
        date=date,
        duration_minutes=duration,
        calories_burnt=calories
    )
        
    db.session.add(new_activity)
    db.session.commit()
    
    return redirect(url_for('main.visualize'))

@main.route('/visualize')
def visualize():
    username = session['username']
    time_period = request.args.get('period', 'week')
    
    # Get current date
    today = datetime.now().date()
    
    # Calculate date range based on time period
    if time_period == 'week':
        start_date = (today - timedelta(days=6)).strftime('%Y-%m-%d')
        date_format = '%a'  # Abbreviated weekday name
    elif time_period == 'month':
        start_date = (today - timedelta(days=29)).strftime('%Y-%m-%d')
        date_format = '%d %b'  # Day and abbreviated month
    elif time_period == 'year':
        start_date = (today - timedelta(days=364)).strftime('%Y-%m-%d')
        date_format = '%b'  # Abbreviated month name
    else:
        start_date = (today - timedelta(days=6)).strftime('%Y-%m-%d')
        date_format = '%a'
    
    # Query data from database
    activities = db.session.query(
        ActivityData, ExerciseType.name.label('exercise_type')
    ).join(
        ExerciseType, ActivityData.exercise_type_id == ExerciseType.id
    ).filter(
        ActivityData.username == username,
        ActivityData.date >= start_date
    ).order_by(
        ActivityData.date
    ).all()
    
    # Format data for template
    formatted_data = []
    for activity, exercise_type in activities:
        date_obj = datetime.strptime(activity.date, '%Y-%m-%d')
        formatted_date = date_obj.strftime(date_format)
        formatted_data.append({
            'date': formatted_date,
            'full_date': activity.date,
            'duration': activity.duration_minutes,
            'calories': activity.calories_burnt,
            'exercise_type': exercise_type
        })
    
    # Pass data to template
    return render_template('visualize.html', 
                           health_data=json.dumps(formatted_data),
                           time_period=time_period,
                           username=session.get('username'))

@main.route('/api/health_data')
def get_health_data():
    username = session['username']
    period = request.args.get('period', 'week')
    
    # Calculate date range based on period
    today = datetime.now().date()
    if period == 'week':
        start_date = (today - timedelta(days=6)).strftime('%Y-%m-%d')
        date_format = '%a'
    elif period == 'month':
        start_date = (today - timedelta(days=29)).strftime('%Y-%m-%d')
        date_format = '%d %b'
    elif period == 'year':
        start_date = (today - timedelta(days=364)).strftime('%Y-%m-%d')
        date_format = '%b'
    else:
        start_date = (today - timedelta(days=6)).strftime('%Y-%m-%d')
        date_format = '%a'
    
    # Get data from database
    activities = db.session.query(
        ActivityData, ExerciseType.name.label('exercise_type')
    ).join(
        ExerciseType, ActivityData.exercise_type_id == ExerciseType.id
    ).filter(
        ActivityData.username == username,
        ActivityData.date >= start_date
    ).order_by(
        ActivityData.date
    ).all()
    
    # Format data for JSON response
    formatted_data = []
    for activity, exercise_type in activities:
        date_obj = datetime.strptime(activity.date, '%Y-%m-%d')
        formatted_date = date_obj.strftime(date_format)
        formatted_data.append({
            'date': formatted_date,
            'full_date': activity.date,
            'duration': activity.duration_minutes,
            'calories': activity.calories_burnt,
            'exercise_type': exercise_type
        })
    
    return jsonify(formatted_data)

@main.route('/api/exercise_types')
def get_api_exercise_types():
    exercise_types = ExerciseType.query.order_by(ExerciseType.name).all()
    return jsonify([{
        'id': et.id,
        'name': et.name,
        'calories_per_minute': et.calories_per_minute
    } for et in exercise_types])

@main.route('/api/calculate_calories')
def api_calculate_calories():
    exercise_type_id = request.args.get('exercise_type_id', type=int)
    duration = request.args.get('duration', type=int)
    
    if not exercise_type_id or not duration:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    exercise_type = ExerciseType.query.get(exercise_type_id)
    if not exercise_type:
        return jsonify({'error': 'Exercise type not found'}), 404
        
    calories = round(exercise_type.calories_per_minute * duration)
    return jsonify({'calories': calories})

@main.route('/share_page')
def share_page():
    return render_template('share_page.html')

@main.route('/health_data', methods=['POST', 'GET'])
def health_data():
    return render_template('health_data.html')


@main.route('/api/share_data', methods=['POST'])
def share_data():
    username = session['username']
    shared_with = request.form.get('shared_with_id')
    content_type = request.form.get('content_type')  # 'activity', 'achievement', 'stats'
    content_id = request.form.get('content_id')
    message = request.form.get('message', '')
    
    # Validate inputs
    if not shared_with or not content_type or not content_id:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if the shared_with user exists
    user_exists = User.query.get(shared_with)
    if not user_exists:
        return jsonify({'error': 'User not found'}), 404
    
    # Store the share in the database
    new_share = SharedContent(
        username = username,
        shared_with_id=shared_with,
        content_type=content_type,
        content_id=content_id,
        message=message,
        share_date=datetime.now().strftime('%Y-%m-%d')
    )
    
    db.session.add(new_share)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Content shared successfully'})

@main.route('/api/shared_with_me')
def shared_with_me():
    username = session['username']
    
    # Get data shared with the current user
    shared_items = db.session.query(
        SharedContent, User.username.label('shared_by_username')
    ).join(
        User, SharedContent.username == User.username
    ).filter(
        SharedContent.shared_with_id == username
    ).order_by(
        SharedContent.share_date.desc()
    ).all()
    
    # Format data for JSON response
    formatted_shared = []
    for shared, username in shared_items:
        formatted_shared.append({
            'id': shared.id,
            'shared_by': username,
            'content_type': shared.content_type,
            'content_id': shared.content_id,
            'message': shared.message,
            'share_date': shared.share_date
        })
    
    return jsonify(formatted_shared)

@main.route('/faqs')
def faqs():
    return render_template('faqs.html')

@main.route('/history')
def history():
    return render_template('history.html')

