
from flask import (Flask, render_template, request, session, redirect, flash, jsonify) 
import json
from model import connect_to_db, db
import crud
from datetime import datetime, date
import os
from passlib.hash import argon2

app = Flask(__name__) 
app.secret_key = os.environ['secret_key']


@app.route("/")
def homepage():
    """homepage for melon calendar"""
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/process-login", methods=["POST"])
def user_login():
    email = request.json.get('email').lower().strip()
    attempt = request.json.get('password')
    user = crud.get_user_by_email(email)
    if not user or not argon2.verify(attempt, user.password):
        return "error"
    else:
        session["user_id"] = user.user_id
        session["fname"] = user.fname
        return "success"
    
@app.route("/book")
def book_tasting():
    today = datetime.today()
    return render_template("calendar.html", today=today)
    

@app.route("/sign-out")
def sign_out_session():
    session.pop("user_id")
    flash("Thanks for coming!", "success")
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        connect_to_db(app) 
        # comment out below when live:
        app.run(host="0.0.0.0", debug=True)

        #comment out below when testing:
        # app.run()