"""Data models for users, appointments"""

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)


    def __repr__(self):
        return f"<User user_id = {self.user_id} email = {self.email} name = {self.fname}>"

class Appt(db.Model):
    __tablename__ = "appts"
    appt_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    client_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    appt_date = db.Column(db.String)
    time_block = db.Column(db.String)

    user = db.relationship("User", primaryjoin = "User.user_id == Appt.client_id")


    def __repr__(self):
        return f"<Appt appt_id = {self.appt_id} client_id = {self.client_id}>"
    

def connect_to_db(app): 

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['POSTGRES_URL']
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    #print statement to show terminal we are connected
    print("Connected to db :)")

if __name__ == "__main__": #importing app from server.py (flask)
    from server import app
    with app.app_context():
        connect_to_db(app)