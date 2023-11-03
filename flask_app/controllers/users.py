from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/logreg")
def loginPage():
    return render_template("login.html")

# Register user info to DB & hash password
@app.route("/register", methods=['POST'])
def create_user():
    if user.User.create_user(request.form):
        return redirect('/animalList')
    return redirect('/logreg')

@app.route("/login", methods = ['POST'])
def login():
    if user.User.login(request.form):
        return redirect("/animalList")
    return redirect("/logreg")

# Logout clear session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")