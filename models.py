from K2_Security import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    is_manager = db.Column(db.Boolean, nullable=False)

    requests = db.relationship('TimeOffRequest', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.phone_number}', '{self.is_manager}')"
     
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  

    user = db.relationship('User', backref='shifts')  

    def __repr__(self):
        return f"Shift('{self.id}')"

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Schedule('{self.user_id}', '{self.shift_id}', '{self.start_time}', '{self.end_time}')"

class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=True)
    salary = db.Column(db.Numeric(10, 2), nullable=True)
    hours_worked = db.Column(db.Numeric(10, 2), nullable=True)
    paid = db.Column(db.Numeric(10, 2), nullable=True)

    def __repr__(self):
        return f"Salary('{self.user_id}', '{self.date}', '{self.salary}', '{self.hours_worked}', '{self.paid}')"

class TimeOffRequest(db.Model):
    __tablename__ = 'TimeOffRequest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    reason = db.Column(db.Text, nullable=True)

    user_requests = db.relationship('User', backref='time_off_requests')

    def __repr__(self):
        return f"TimeOffRequest('{self.user_id}', '{self.start_date}', '{self.end_date}', '{self.reason}')"

