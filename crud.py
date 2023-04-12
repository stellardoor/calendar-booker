from model import db, User, Appt,  connect_to_db

def create_user(email, password, fname, lname):
    user = User(
        email=email, 
        password=password, 
        fname=fname,
        lname = lname
        )
    db.session.add(user)
    db.session.commit()

def get_user_by_email(email):
    user = User.query.filter(User.email == email).first()

    return user

def create_appt(user_id, appt_date, time_block):
    appt = Appt(
        client_id = user_id,
        appt_date = appt_date,
        time_block = time_block
    )
    db.session.add(appt)
    db.session.commit()

def load_avail_appts_by_time(date, start_time, end_time):
    "loads list of appt"
    all_appt_on_date = Appt.query.filter(Appt.appt_date == date).all()
    appts_data = []
    for appt in all_appt_on_date:
        if appt.time_block >= start_time and appt.time_block <= end_time:
            appts_data.append(appt)
    return appts_data


if __name__ == "__main__":
    from server import app
    with app.app_context(): #importing app from server.py (flask)

        connect_to_db(app)