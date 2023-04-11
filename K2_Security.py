from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gv64woe1'
app.config['MYSQL_DB'] = 'k2_security'
app.secret_key = 'your_secret_key'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('ManagerHome.html')
    else:
        return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    password_hash = hashlib.md5(password.encode()).hexdigest()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password_hash))
    user = cur.fetchone()
    cur.close()
    if user:
        # Login successful, store the username in a session variable
        session['username'] = username
        return redirect(url_for('home'))
    else:
        # Login unsuccessful, redirect back to login page
        return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    password_hash = hashlib.md5(password.encode()).hexdigest()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hash))
    mysql.connection.commit()
    cur.close()
    # Registration successful, redirect to login page
    return redirect(url_for('login'))

@app.route('/shifts', methods=['POST'])
def create_shift():
    date = request.form['date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO shifts (date, start_time, end_time, description) VALUES (%s, %s, %s, %s)",
                (date, start_time, end_time, description))
    mysql.connection.commit()
    cur.close()
    # Shift creation successful, redirect to schedule page
    return redirect(url_for('schedule'))

@app.route('/shifts', methods=['GET'])
def get_shifts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shifts")
    shifts = cur.fetchall()
    cur.close()
    return jsonify(shifts)

@app.route('/schedule')
def schedule():
    if 'username' in session:
        return render_template('ManagerSchedule.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session and redirect to login page
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)