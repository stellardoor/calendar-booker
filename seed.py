"""adding users to test and """

import os # operating system - establishes interaction between the user and the operating system


import crud
import model
from datetime import date
import json
from passlib.hash import argon2
from server import app

os.system("dropdb melon-appt")
os.system("createdb melon-appt")


def add_test_users():
    for num in range(10):
        email = f"user{num}@testing.com".lower()
        password = argon2.hash("testing")
        fname = f"user{num}"
        lname = f"lastname{num}"

        user = crud.create_user(email, password, fname, lname)

    

with app.app_context():
    model.connect_to_db(app)
    model.db.create_all()
    add_test_users()