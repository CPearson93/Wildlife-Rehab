from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")