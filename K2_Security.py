from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gv64woe1'
app.config['MYSQL_DB'] = 'k2_security'

mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the request body
    username = request.json.get('username')
    password = request.json.get('password')

    # Create a cursor and execute a SELECT query to check if the username and password are correct
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))

    # Fetch the result of the query
    result = cur.fetchone()

    # Close the cursor
    cur.close()

    # If the query returns a result, return a success response
    if result:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)

