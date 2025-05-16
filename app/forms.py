# for CSRF protection
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')


class RegisterForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')

