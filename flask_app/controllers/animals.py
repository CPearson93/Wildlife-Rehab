from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import animal

@app.route("/animalList")
def animalList():
    if 'user_id' not in session: return redirect('/')
    return render_template("animalList.html")