# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from app import db

main = Blueprint('main', __name__)

@main.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        flash('Login successful!', 'success')
        return redirect(url_for('main.dashboard'))  # redirect to dashboard
    else:
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('main.account'))

@main.route('/account')
def account():
    return render_template('account.html')

@main.route('/dashboard')
def dashboard():
    return render_template('health_data.html')
