from K2_Security import app, db, mail
from models import User, Shift, TimeOffRequest
from forms import LoginForm, RegistrationForm, ShiftForm, TimeOffForm
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@login_required
def home_view():
    if current_user.is_manager:
        shifts = Shift.query.all()  
        return render_template('ManagerHome.html', shifts=shifts)
    else:
        shifts = Shift.query.filter_by(user_id=current_user.id).all()  
        return render_template('EmployeeSchedule.html', shifts=shifts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('home_view'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    form.email.label.text = 'Username (Email address)'  
    return render_template('login.html', title='Login', form=form)
    

@app.route("/logout")
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        is_manager = form.role.data == 'Manager'
        user = User(username=form.email.data, email=form.email.data, password=hashed_password, phone_number=form.phone_number.data, is_manager=is_manager)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule_view():
    if current_user.is_manager:
        form = ShiftForm()
        if form.validate_on_submit():
            shift = Shift(start_time=form.start_time.data, end_time=form.end_time.data, date=form.date.data, user_id=form.user_id.data)
            db.session.add(shift)
            db.session.commit()
            flash('Shift has been added!', 'success')
            return redirect(url_for('schedule_view'))
        shifts = Shift.query.all()
        return render_template('ManagerSchedule.html', title='Schedule Management', shifts=shifts, form=form)
    else:
        shifts = Shift.query.filter_by(user_id=current_user.id).all()  
        return render_template('EmployeeSchedule.html', shifts=shifts)

@app.route('/manager/users', methods=['GET', 'POST'])
@login_required
def manager_users():
    users = User.query.all()
    return render_template('ManagerUsers.html', title='User Management', users=users)

@app.route('/generate_reports', methods=['GET', 'POST'])
@login_required
def generate_reports():
    if current_user.is_manager:
        return render_template('ManagerHome.html', title='Generate Reports')
    else:
        return redirect(url_for('home_view'))


@app.route('/manager_schedule', methods=['GET', 'POST'])
@login_required
def manager_schedule():
    if current_user.is_manager:
        shifts = Shift.query.all()
        return render_template('ManagerSchedule.html', title='Employee Schedules', shifts=shifts)
    else:
        return redirect(url_for('home_view'))


@app.route('/time_off_requests', methods=['GET', 'POST'])
@login_required
def time_off_requests():
    if current_user.is_manager:
        requests = TimeOffRequest.query.all()
        return render_template('TimeOffRequests.html', title='Time Off Requests', requests=requests)
    else:
        
        requests = TimeOffRequest.query.filter_by(user_id=current_user.id).all()
        return render_template('TimeOffRequests.html', title='My Time Off Requests', requests=requests)



@app.route('/request_off', methods=['GET', 'POST'])
@login_required
def request_off_view():
    form = TimeOffForm()
    if form.validate_on_submit():
        request_off = TimeOffRequest(start_date=form.start_date.data, end_date=form.end_date.data, reason=form.reason.data, user_id=current_user.id)
        db.session.add(request_off)
        db.session.commit()
        flash('Time off request has been sent!', 'success')
        return redirect(url_for('home_view'))
    return render_template('EmployeeSchedule.html', title='Request Time Off', form=form)