from flask import Flask, render_template, request, redirect, session
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = "secret key"

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="gv64woe1",
  database="K2_Security"
)
mycursor = mydb.cursor()

@app.route("/")
def home():
    if 'username' in session:
        return redirect("/Home")
    else:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        password = hashlib.md5(password.encode()).hexdigest()

        sql = "SELECT * FROM user WHERE username=%s AND password=%s"
        val = (username, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['type'] = user[3]
            return redirect("/Home")
        else:
            return render_template("login.html", error="Invalid Username or Password")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('type', None)
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        
        password = hashlib.md5(password.encode()).hexdigest()

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        role = request.form["role"]
        
        sql = "INSERT INTO user (username, password, type) VALUES (%s, %s, %s)"
        val = (username, password, role.lower() == "manager")
        mycursor.execute(sql, val)
        mydb.commit()
        
        user_id = mycursor.lastrowid

        sql = "INSERT INTO user_details (id, name, email, phone, address) VALUES (%s, %s, %s, %s, %s)"
        val = (user_id, name, email, phone, address)
        mycursor.execute(sql, val)
        mydb.commit()

        return redirect("/login")
    else:
        return render_template("registration.html")

@app.route("/Home")
def manager_home():
    if 'username' in session and session['type']:
        return render_template("ManagerHome.html")
    else:
        return redirect("/login")

@app.route("/Schedules")
def manager_schedule():
    if 'username' in session and session['type']:
        return render_template("ManagerSchedule.html")
    else:
        return redirect("/login")

@app.route("/Schedules", methods=["GET", "POST"])
def create_shift():
    if request.method == "POST":
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        date = request.form["date"]

        sql = "INSERT INTO shifts (start_time, end_time, date) VALUES (%s, %s, %s)"
        val = (start_time, end_time, date)
        mycursor.execute(sql, val)
        mydb.commit()

        return redirect("/Schedules")
    else:
        return render_template("ManagerSchedule.html")

if __name__ == '__main__':
    app.run(debug=True)
