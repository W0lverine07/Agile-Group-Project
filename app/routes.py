from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.db_helper import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from datetime import datetime, timedelta
from app.models import db, UserDetails, User
from flask import jsonify
from app.models import db, User, ExerciseType, ActivityData, SharedContent
import random, json

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('login.html')

#generate a unique user ID for the new user
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
        flash("Login successful!", "success")
        return redirect(url_for('main.health_data'))
    else:
        flash("Invalid username or password", "error")
        return redirect(url_for('main.home'))


@main.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.home'))

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

        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.health_data'))
    except Exception as e:
        flash(f"Error saving profile: {e}", "error")
        return redirect(url_for('main.edit_profile'))
#end of the profile page logic

@main.route('/account')
def account():
    return render_template('account.html')

@main.route('/upload')
def upload():
    # Get exercise types for the dropdown
    exercise_types = ExerciseType.query.order_by(ExerciseType.name).all()
    return render_template('upload.html', exercise_types=exercise_types, today=datetime.now().strftime('%Y-%m-%d'))

@main.route('/upload_data', methods=['POST'])
def upload_data():
    user_id = session['user_id']
    exercise_type_id = request.form.get('exercise_type', type=int)
    duration = request.form.get('duration', type=int)
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Validate inputs
    if not exercise_type_id or not duration:
        flash("Exercise type and duration are required", "error")
        return redirect(url_for('main.upload'))
    
    # Calculate calories based on exercise type and duration
    exercise_type = ExerciseType.query.get(exercise_type_id)
    calories = round(exercise_type.calories_per_minute * duration)
    
    # Insert the activity data
    new_activity = ActivityData(
        user_id=user_id, 
        exercise_type_id=exercise_type_id,
        date=date,
        duration_minutes=duration,
        calories_burnt=calories
    )
    
    db.session.add(new_activity)
    db.session.commit()
    
    # flash("Activity data added successfully!", "success")
    return redirect(url_for('main.visualize'))

@main.route('/visualize')
def visualize():
    user_id = session['user_id']
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
        ActivityData.user_id == user_id,
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
                           user_id=user_id,
                           username=session.get('username'))

@main.route('/api/health_data')
def get_health_data():
    user_id = session['user_id']
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
        ActivityData.user_id == user_id,
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
    user_id = session['user_id']
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
        user_id=user_id,
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
    user_id = session['user_id']
    
    # Get data shared with the current user
    shared_items = db.session.query(
        SharedContent, User.username.label('shared_by_username')
    ).join(
        User, SharedContent.user_id == User.id
    ).filter(
        SharedContent.shared_with_id == user_id
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

