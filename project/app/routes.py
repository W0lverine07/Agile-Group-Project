from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.db_helper import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')

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

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

    if user:
        conn.close()
        flash("Username already exists", "error")
        return redirect(url_for('main.home'))

    hashed_pw = generate_password_hash(password)
    conn.execute('INSERT INTO user (username, password_hash) VALUES (?, ?)', (username, hashed_pw))
    conn.commit()
    conn.close()

    flash("Registration successful! Please log in.", "success")
    return redirect(url_for('main.home'))

@main.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        flash("Login successful!", "success")
        return redirect(url_for('main.account'))
    else:
        flash("Invalid username or password", "error")
        return redirect(url_for('main.home'))


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

@main.route('/login')
def history():
    return render_template('login.html')

