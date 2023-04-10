from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gv64woe1'
app.config['MYSQL_DB'] = 'k2_security'

mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    address = request.json.get('address')
    role = request.json.get('role')

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user (username, password, type) VALUES (%s, %s, %s)", (username, hashed_password, role))
    user_id = cur.lastrowid

    cur.execute("INSERT INTO user_details (id, name, email, phone, address) VALUES (%s, %s, %s, %s, %s)", (user_id, name, email, phone, address))

    cur.execute("INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)", (user_id, role))

    mysql.connection.commit()
    cur.close()

    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, hashed_password))

    result = cur.fetchone()

    cur.close()

    if result:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/shifts', methods=['POST'])
def create_shift():
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO shift (start_time, end_time) VALUES (%s, %s)", (start_time, end_time))

    mysql.connection.commit()
    cur.close()

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
