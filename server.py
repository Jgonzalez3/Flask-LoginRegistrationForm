from flask import Flask, redirect, render_template, request, session, flash
from mysqlconnection import MySQLConnection
import md5, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "secret"
mysql = MySQLConnection(app, 'login_reg')
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create_user():
    errors = []
    firstname = request.form['first_name']
    session['firstname'] = firstname
    lastname = request.form['last_name']
    session['lastname'] = lastname
    email = request.form['email']
    password = md5.new(request.form['password']).hexdigest()
    if len(request.form['first_name']) < 2:
        errors.append("First Name must have at least 2 characters")
    for i in range(0,len(firstname)):
        if firstname[i] == "1" or firstname[i] == "2" or firstname[i] == '3' or firstname[i] == '4' or firstname[i] == '5' or firstname[i] == '6' or firstname[i] == '7' or firstname[i] == '8' or firstname[i] == '9' or firstname[i] == '0':
            errors.append("First Name can only contain letters")
    if len(request.form['last_name']) < 2:
        errors.append("Last Name must have at least 2 characters")
    for i in range(0,len(lastname)):
        if lastname[i] == "1" or lastname[i] == "2" or lastname[i] == '3' or lastname[i] == '4' or lastname[i] == '5' or lastname[i] == '6' or lastname[i] == '7' or lastname[i] == '8' or lastname[i] == '9' or lastname[i] == '0':
            errors.append("Last Name can only contain letters")
    if not EMAIL_REGEX.match(request.form['email']):
        errors.append("Email is Invalid")
    if len(request.form["password"]) < 8:
        errors.append("Password Must Contain More than 8 Characters")
    if request.form["pw_confirm"] != request.form["password"]:
        errors.append("Passwords Do Not Match Re-enter")
    if len(errors) > 0:
        for error in errors:
            flash(error)
        return redirect("/")

    insert_query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
    data = {'first_name': firstname, 'last_name': lastname, 'email': email, 'password': password }
    mysql.query_db(insert_query, data)
    
    return redirect("/success")

@app.route("/login", methods = ['POST'])
def login():
    errors = []
    email = request.form['email']
    password = md5.new(request.form['password']).hexdigest()
    query = "SELECT * FROM users WHERE users.email = :email AND users.password = :password"
    data = {'email': email, 'password': password }
    valid = mysql.query_db(query, data)
    # print valid
    # print data
    if valid == []:
        errors.append("Invalid Email or Password")
    elif password == valid[0]['password'] and email == valid[0]["email"]:
        return redirect("/success")
    if len(errors) > 0:
        for error in errors:
            flash(error)
        return redirect("/")

@app.route("/success")
def success():
    return render_template("success.html")
app.run(debug=True)
