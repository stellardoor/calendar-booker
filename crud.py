from model import db, User, Appt, connect_to_db
from datetime import datetime
import json


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

def get_time_slots_for_form():
    time_list = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    time_slot_list = []

    am_i= 0
    for num in time_list:
        time_slot_list.append([f"{am_i}:00" , f"{num}:00am"])
        time_slot_list.append([f"{am_i}:30" , f"{num}:30am"])
        am_i +=1
    
    pm_i = 12
    for num in time_list:
        time_slot_list.append([f"{pm_i}:00" , f"{num}:00pm"])
        time_slot_list.append([f"{pm_i}:30" , f"{num}:30pm"])
        pm_i +=1

    return time_slot_list

# def get_time_slots_for_appts():
#     time_slots = []
#     for num in range(24):
#         time_slots.extend([f"{num}:00", f"{num}:30"])
#     return time_slots
     

def get_time_slots_by_calendar_input(date, start_time, end_time):
    """loads list of appts for /book-tasting"""
    already_scheduled_appts = Appt.query.filter(Appt.appt_date == date).all()
    scheduled_appts_times = []

    for appt in already_scheduled_appts:
        scheduled_appts_times.append(appt.time_block)

    avail_slots = []
    all_time_slots = get_time_slots_for_form()
    time_format = "%H:%M"
    start = datetime.strptime(start_time, time_format)
    end = datetime.strptime(end_time, time_format)

    for slot in all_time_slots:
        slot_time = datetime.strptime(slot[0], time_format)
        if slot_time >= start and slot_time <= end:
            if slot[0] not in scheduled_appts_times:
                avail_slots.append(slot)
    return avail_slots

def already_has_appt_by_date(user_id, date):
    """takes in user_id and returns true if they already have an appt booked on that date"""
    check_appt = Appt.query.filter(db.and_(Appt.appt_date == date, Appt.client_id == user_id)).first()
    if check_appt:
        return True
    return False

def create_tasting_appointment(client_id, appt_date, time_block, time_block12hr):
    appt = Appt(
        client_id = client_id,
        appt_date = appt_date,
        time_block = f'["{time_block}", "{time_block12hr}"]'
    )
    db.session.add(appt)
    db.session.commit()

def get_all_users_bookings(user_id):
    user_appts = Appt.query.filter(Appt.client_id == user_id).all()
    appts_list = []
    for appt in user_appts:
        appt_dict = turn_appt_to_dict(appt)
        appts_list.append(appt_dict)

    return appts_list

def turn_appt_to_dict(appt):
    appt_dict = {}
    appt_dict["appt_date"] = appt.appt_date
    time_block = json.loads(appt.time_block)
    appt_dict["time_block"] = time_block[1]

    return appt_dict



if __name__ == "__main__":
    from server import app
    with app.app_context(): #importing app from server.py (flask)

        connect_to_db(app)