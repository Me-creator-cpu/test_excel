import streamlit as st
import datetime
from datetime import timedelta
from streamlit_calendar import calendar
import csv
import pandas as pd
import re
#from pytz import timezone


# https://ryanandmattdatascience.com/streamlit-calender/
# https://github.com/kanishtulasi/Meeting_Room_Booking_System/blob/main/meeting_room.py
# => https://meeting-room-booking-system-kt.streamlit.app/
# https://docs.python.org/fr/3/library/calendar.html
# https://github.com/im-perativa/streamlit-calendar

# Get the current time in IST
#current_time_ist = datetime.datetime.now(ist)
current_time_ist = datetime.datetime.now()
ctif = current_time_ist.strftime("%y-%m-%d %H:%M:%S")
default_time_gap=15
calendar_options = {
    "editable": True,
    "selectable": True,
    "initialView": "timeGridWeek",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,listMonth,resourceTimelineDay"
        #"right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    }
}

calendar_options_v2 = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "timeGridWeek,resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "timeGridWeek",
    "nowIndicator": True,
    "resourceGroupField": "cours",
    "resources": [
        {"id": "a", "cours": "Cours 1", "title": "Kid A", "color": "#FF6C6C"},
        {"id": "b", "cours": "Cours 1", "title": "Kid B"},
        {"id": "c", "cours": "Cours 2", "title": "Kid C"},
        {"id": "d", "cours": "Cours 2", "title": "Kid D"},
        {"id": "e", "cours": "Cours 3", "title": "Kid E"},
        {"id": "f", "cours": "Cours 4", "title": "Kid F"},
    ],
}

# Book a Room
# Define a dictionary that maps room names to their capacities
room_capacity = {
    "Room 1": 6,
    "Room 2": 8,
    "Room 3": 10,
    "Room 4": 12,
    "Room 5": 14,
}

# Calendar Default Events
calendar_events = [
    {
        "title": "Event 1",
        "start": "2026-05-11T09:30:00",
        "end": "2026-05-11T10:00:00",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "start": "2026-05-11T09:30:00",
        "end": "2026-05-11T10:00:00",
        "resourceId": "b",
    },
    {
        "title": "Event 3",
        "start": "2026-05-11T14:00:00",
        "end": "2026-05-11T14:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 4",
        "start": "2026-05-11T14:00:00",
        "end": "2026-05-11T14:30:00",
        "resourceId": "c",
    },
    {
        "title": "Event 5",
        "start": "2026-05-11T10:00:00",
        "end": "2026-05-11T10:30:00",
        "resourceId": "d",
    }
]

calendar_custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""
# Define file paths for storing booking data
booking_data_file = "booking_data.csv"

# Load existing booking data from the CSV file
try:
    with open(booking_data_file, "r") as file:
        reader = csv.DictReader(file)
        booking_data = {"room_bookings": {}, "room_availability": {}}

        for row in reader:
            booking_id = int(row["booking_id"])
            booking_data["room_bookings"][booking_id] = {
                "booking_id": booking_id,
                "date": row["date"],
                "start_time": row["start_time"],
                "end_time": row["end_time"],
                "room": row["room"],
                "name": row["name"],
                "email": row["email"],
                "description": row["description"],
            }

            # Update room availability data
            if row["date"] not in booking_data["room_availability"]:
                booking_data["room_availability"][row["date"]] = {}
            if row["room"] not in booking_data["room_availability"][row["date"]]:
                booking_data["room_availability"][row["date"]][row["room"]] = []
            booking_data["room_availability"][row["date"]][row["room"]].append(
                (row["start_time"], row["end_time"])
            )

except FileNotFoundError:
    booking_data = {"room_bookings": {}, "room_availability": {}}

# Utility Functions
def is_valid_time(time_str):
    try:
        datetime.datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def is_room_available(date, start_time, end_time, room):
    if date not in booking_data["room_availability"]:
        return True

    if room not in booking_data["room_availability"][date]:
        return True

    for booking in booking_data["room_availability"][date][room]:
        b_start_time, b_end_time = booking
        if not (end_time <= b_start_time or start_time >= b_end_time):
            return False

    return True

# Generate a random 4-digit booking ID
def generate_random_booking_id():
    return random.randint(1000, 9999)

# Calendar Functions
def resa_book():
    st.header("New event")
    current_date = current_time_ist.date()
    current_time = current_time_ist.time()
    office_start_time = datetime.time(9, 0)
    office_end_time = datetime.time(18, 0)
    default_time_gap=15
    if default_time_gap < 15:
        default_time_gap=15

    date = st.date_input("Select the Date:", min_value=current_date,value=current_date)
    if date:
        start_times = [office_start_time]
        while start_times[-1] < office_end_time:
            next_time = (datetime.datetime.combine(date, start_times[-1]) + timedelta(minutes=default_time_gap)).time()
            start_times.append(next_time)  
      
        start_time = st.selectbox("Select the Start Time:", start_times,index=None)
        current_time = current_time_ist.time()
        if start_time:
            if (date == current_date and start_time < current_time):
                st.warning("Start time should be from current date and time.")
            else:
                end_of_day = min(office_end_time, datetime.time(23, 59))
                available_end_times = [datetime.datetime.combine(date, start_time) + timedelta(minutes=i) for i in range(default_time_gap, (end_of_day.hour - start_time.hour) * 60 + 1, default_time_gap)]
                formatted_end_times = [et.strftime('%H:%M:%S') for et in available_end_times]
                end_time = st.selectbox("Select the End Time:", formatted_end_times,index=None)                
                if end_time:
                    available_room_options = []
                    for room, capacity in room_capacity.items():
                        if is_room_available(str(date), str(start_time), str(end_time), room):
                            available_room_options.append(f"{room} (Capacity: {capacity})")

                    if not available_room_options:
                        st.warning("Rooms are not available during this time.")
                    else:
                        st.info("Available Rooms")
                        room_choice = st.selectbox("Select a Room:", available_room_options,index=None)
                        if room_choice:
                            st.subheader('Enter Booking Details')
                            # Extract the selected room name (excluding the capacity information)
                            selected_room = room_choice.split(" (Capacity: ")[0]
                            description = st.text_input("Enter Meeting Title:")
                            name = st.text_input("Enter your Name:")
                            email = st.text_input("Enter your Email:")
                            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                                st.warning("Please enter a valid email address.")
                                return
                            
                            if not name or not description:
                                st.warning("All details are mandatory.")
                            else:
                                if st.button("Book Room"):
                                    booking_id = generate_random_booking_id()  # Generate a random 4-digit booking ID
                                    booking_data["room_bookings"][booking_id] = {
                                    "date": str(date),
                                    "start_time": str(start_time),
                                    "end_time": str(end_time),
                                    "room": selected_room,  # Use the extracted room name
                                    "name": name,
                                    "email": email,
                                    "description": description,
                                    }
                                    if str(date) not in booking_data["room_availability"]:
                                        booking_data["room_availability"][str(date)] = {}
                                    if selected_room not in booking_data["room_availability"][str(date)]:
                                        booking_data["room_availability"][str(date)][selected_room] = []
                                    booking_data["room_availability"][str(date)][selected_room].append((str(start_time), str(end_time)))


st.title("Planning")

planning = calendar(
        events=calendar_events, 
        options=calendar_options_v2,
        custom_css=calendar_custom_css,
        key="basic_cal"
        )

if st.button('Ungroup'):
    planning.resourceGroupField=None

st.write("Calendar data:", planning)
btn_txt_book='Book a meeting 🗓️'
menu_choice = st.selectbox("Menu", [btn_txt_book, "Cancel Booking", "View Bookings"])
if menu_choice == btn_txt_book:
    resa_book()

