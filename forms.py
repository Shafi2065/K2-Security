from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
import re
from models import User

def validate_password(form, field):
    password = field.data
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[@$!%*?&]', password):
        raise ValidationError('Password should have at least 8 characters, 1 capital letter, 1 special symbol, and a mix of letters and numbers.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Invalid email or password.')


class RegistrationForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), validate_password])
    phone_number = StringField('Phone Number')
    role = SelectField('Role', choices=[('Employee', 'Employee'), ('Manager', 'Manager')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ShiftForm(FlaskForm):
    start_time = StringField('Start Time (hh:mm)', validators=[DataRequired(), Length(min=5, max=5)])
    end_time = StringField('End Time (hh:mm)', validators=[DataRequired(), Length(min=5, max=5)])
    date = StringField('Date (yyyy-mm-dd)', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Create Shift')

class TimeOffForm(FlaskForm):
    name = StringField('First Name and Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=6, max=20)])
    contact_method = SelectField('Contact method upon reply', choices=[('phone', 'Phone'), ('email', 'Email'), ('none', 'Do not contact')], validators=[DataRequired()])
    holiday_start = StringField('Holiday From (yyyy-mm-dd)', validators=[DataRequired(), Length(min=10, max=10)])
    holiday_end = StringField('Holiday End (yyyy-mm-dd)', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Submit')