from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gv64woe1'
app.config['MYSQL_DB'] = 'k2_security'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('ManagerHome.html')

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
        return redirect(url_for('home'))
    else:
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
    return render_template('ManagerSchedule.html')

if __name__ == '__main__':
    app.run(debug=True)