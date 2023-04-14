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
        email_address = request.form.get("email_address")
        password = request.form.get("password")
        phone_number = request.form.get("phone_number")
        role = request.form.get("role")
        
        if role is not None:
            is_manager = (role.lower() == "manager")
        else:
            is_manager = False
        
        try:
            sql = "INSERT INTO user (email_address, password, phone_number, is_manager) VALUES (%s, %s, %s, %s)"
            val = (email_address, hashlib.md5(password.encode()).hexdigest(), phone_number, is_manager)
            mycursor.execute(sql, val)
            mydb.commit()
        except:
            mydb.rollback()
            return render_template("registration.html", error="An error occurred while processing your request.")
        
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
        sql = "SELECT * FROM shifts"
        mycursor.execute(sql)
        shifts = mycursor.fetchall()
        return render_template("ManagerSchedule.html", shifts=shifts)
    else:
        return redirect("/login")

@app.route("/Schedules/create", methods=["GET", "POST"])
def create_shift():
    if request.method == "POST":
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        date = request.form.get("date")

        sql = "INSERT INTO shifts (start_time, end_time, date) VALUES (%s, %s, %s)"
        val = (start_time, end_time, date)
        mycursor.execute(sql, val)
        mydb.commit()

        return redirect("/Schedules")
    else:
        return render_template("CreateShift.html")

@app.route("/Schedules/<int:id>/edit", methods=["GET", "POST"])
def edit_shift(id):
    if 'username' in session and session['type']:
        if request.method == "POST":
            start_time = request.form.get("start_time")
            end_time = request.form.get("end_time")
            date = request.form.get("date")

            sql = "UPDATE shifts SET start_time=%s, end_time=%s, date=%s WHERE id=%s"
            val = (start_time, end_time, date, id)
            mycursor.execute(sql, val)
            mydb.commit()

            return redirect("/Schedules")
        else:
            sql = "SELECT * FROM shifts WHERE id=%s"
            val = (id,)
            mycursor.execute(sql, val)
            shift = mycursor.fetchone()
            return render_template("EditShift.html", shift=shift)
    else:
        return redirect("/login")


@app.route("/Schedules/int:id/delete")
def delete_shift(id):
    if 'username' in session and session['type']:
        sql = "DELETE FROM shifts WHERE id=%s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect("/Schedules")
    else:
        return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
