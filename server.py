
from flask import (Flask, render_template, request, session, redirect, flash, jsonify) 
import json
from model import connect_to_db, db
import crud
from datetime import datetime, date, timedelta
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
    today = date.today()
    tomorrow = today + timedelta(1)
    time_slot_list = crud.get_time_slots_for_form()
    return render_template("calendar.html", tomorrow=tomorrow, time_slot_list=time_slot_list)

@app.route("/get-time-windows", methods=["POST"])
def load_time_slots_by_calendar():
    """takes in calendar change from user, and loads only available slots for that day"""
    date_input = request.json.get("date-input")
    start_time_input = request.json.get("start-time-input")
    end_time_input = request.json.get("end-time-input")
    time_format = "%H:%M"

    if datetime.strptime(start_time_input, time_format) > datetime.strptime(end_time_input, time_format):
        return jsonify(["time-error"])
    
    time_slots = crud.get_time_slots_by_calendar_input(date_input, start_time_input, end_time_input)

    if time_slots == []:
        return jsonify(["empty"])
    
    return jsonify(time_slots)

@app.route("/book-tasting", methods=["POST"])
def schedule_tasting():
    """takes in time slot submission and books the appointment - will not book an appt with no date / time submitted, or if the user already has an appt on that date"""
    client_id = session["user_id"]
    appt_date = request.json.get("date-input")
    appt_time = request.json.get("appt-time")
    appt_time12hr = request.json.get("appt-time-12hr")
    if not appt_time:
        return jsonify(["no-time"])
    
    if not appt_date:
        return jsonify(["no-date"])
    
    check_user_appt = crud.already_has_appt_by_date(client_id, appt_date)

    if check_user_appt:
        return jsonify(["user-error"])
    else:
        crud.create_tasting_appointment(client_id, appt_date, appt_time, appt_time12hr)
        
        return jsonify(["success"])
    

@app.route("/tastings")
def view_tastings():
    """page that shows users current bookings"""
    bookings = crud.get_all_users_bookings(session["user_id"])
    return render_template("appts.html", bookings = bookings)

@app.route("/sign-out")
def sign_out_session():
    session.pop("user_id")
    flash("See ya later!", "success")
    return redirect("/")


if __name__ == "__main__":
    # with app.app_context():
    connect_to_db(app) 
    # comment out below when live:
    # app.run(host="0.0.0.0", debug=True)

    #comment out below when testing:
    app.run(host="0.0.0.0")