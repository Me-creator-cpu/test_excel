import streamlit as st
#import datetime
from datetime import timedelta
from datetime import datetime
from datetime import time
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
# https://github.com/im-perativa/streamlit-calendar-demo/blob/main/demo.py
# https://fullcalendar.io/docs/resourceAreaColumns-grouping-demo

# Get the current time in IST
#current_time_ist = now(ist)
current_time_ist = now()
ctif = current_time_ist.strftime("%y-%m-%d %H:%M:%S")

businessHours = [
  {
    "daysOfWeek": [ 1, 2, 3 ],  # Monday, Tuesday, Wednesday
    "startTime": '08:00',       # 8am
    "endTime": '18:00'          # 6pm
  },
  {
    "daysOfWeek": [ 4, 5 ],     # Thursday, Friday
    "startTime": '09:00',       # 9am
    "endTime": '16:00'          # 4pm
  }
]

default_time_gap=15
initialDate='2026-05-12'
calendar_groupby = "level" #"title" #"building"

calendar_display={
        "daygrid":"Day",
        "timegrid":"Time",
        "timeline":"Timeline",
        "resource-daygrid":"Resource: Day",
        "resource-timegrid":"Resource: Time",
        "resource-timeline":"Resource: Timeline",
        "list":"List",
        "multimonth":"Multi months",
}

calendar_eventTimeFormat= { # like '14:30:00'
    "hour": '2-digit',
    "minute": '2-digit',
    "second": '2-digit',
    "hour12": False
  }
data_type={
    "Color":["#2784F5","#F54927",    "#EEF527",    "#F57D27",    "#27F549"]
}  
calendar_resources = [
    {"id": "a", "title": "Kid A", "level":"Niveau 2", "color": "#2784F5"},
    {"id": "b", "title": "Kid B", "level":"Niveau 1", "color": "#F54927"},
    {"id": "c", "title": "Kid C", "level":"Niveau 3", "color": "#EEF527"},
    {"id": "d", "title": "Kid D", "level":"Niveau 5", "color": "#FFBD45"},
    {"id": "e", "title": "Kid E", "level":"Niveau 8", "color": "#FF6C6C"},
    {"id": "f", "title": "Kid F", "level":"Niveau 4", "color": "#3DD56D"},
    {"id": "g", "title": "Kid G", "level":"Niveau 3", "color": "#27F549"},
]

calendar_events = [
    {"resourceId": "a", "cours": "Cours 1", "title": "Kid A", "start": "2026-05-12T09:30:00", "end": "2026-05-12T10:00:00", "color": "#2784F5", "backgroundColor": "#FF6C6C", "borderColor": "#FF6C6C"},
    {"resourceId": "b", "cours": "Cours 1", "title": "Kid B", "start": "2026-05-12T09:30:00", "end": "2026-05-12T10:00:00", "color": "#F54927"},
    {"resourceId": "c", "cours": "Cours 2", "title": "Kid C", "start": "2026-05-12T10:30:00", "end": "2026-05-12T11:00:00", "color": "#EEF527"},
    {"resourceId": "d", "cours": "Cours 2", "title": "Kid D", "start": "2026-05-12T14:00:00", "end": "2026-05-12T14:30:00", "color": "#FFBD45"},
    {"resourceId": "e", "cours": "Cours 3", "title": "Kid E", "start": "2026-05-12T14:30:00", "end": "2026-05-12T15:00:00", "color": "#FF6C6C"},
    {"resourceId": "f", "cours": "Cours 4", "title": "Kid F", "start": "2026-05-12T15:30:00", "end": "2026-05-12T16:00:00", "color": "#3DD56D"},
]

data_cours = [
    {"title": "Title 1", "niveau": "1", "start": "2026-05-12 09:30:00", "end": "2026-05-12T10:00:00"},
    {"title": "Title 2", "niveau": "2", "start": "2026-05-12 10:30:00", "end": "2026-05-12 11:00:00"},
    {"title": "Title 3", "niveau": "3", "start": "2026-05-12 14:30:00", "end": "2026-05-12 15:00:00"},
    {"title": "Title 4", "niveau": "4", "start": "2026-05-12 15:30:00", "end": "2026-05-12 16:00:00"},
    {"title": "Title 5", "niveau": "5", "start": "2026-05-18 09:30:00", "end": "2026-05-18 10:00:00"},
    {"title": "Title 6", "niveau": "6", "start": "2026-05-19 10:30:00", "end": "2026-05-19 11:00:00"},
    {"title": "Title 7", "niveau": "7", "start": "2026-05-20 14:30:00", "end": "2026-05-20 15:00:00"},
    {"title": "Title 8", "niveau": "0", "start": "2026-05-21 15:30:00", "end": "2026-05-21 16:00:00"},
]

data_cours_niveau = {
	"niveau_txt":["Pour tous","Niveau 1","Niveau 2","Niveau 3","Niveau 4","Niveau 5","Niveau 6","Niveau 7","Niveau 8","Niveau 9","Niveau 1O","Niveau 11","Niveau 12"],
	"niveau_lvl":[0,1,2,3,4,5,6,7,8,9,10,11,12]
}

liste_niveaux = {
	"Pour tous":0,
	"Niveau 1":1,
	"Niveau 2":2,
	"Niveau 3":3,
	"Niveau 4":4,
	"Niveau 5":5,
	"Niveau 6":6,
	"Niveau 7":7,
	"Niveau 8":8,
	"Niveau 9":9,
	"Niveau 1O":10,
	"Niveau 11":11,
	"Niveau 12":12
}

calendar_options_demo = {
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

calendar_options = {
    "editable": True,
    "navLinks": True,
    "resources": calendar_resources,
    "eventTimeFormat": calendar_eventTimeFormat,
    "selectable": True,
    "nowIndicator": True,
    "eventOrder":"level,-duration,allDay,start",
    "eventDisplay":"block",
    #"resourceGroupField": calendar_groupby,
    "resourceAreaWidth": "40%",
    "resourceAreaColumns": [
      {
        "group": True,
        "field": "level",
        "headerContent": "Level"
      },
      {
        "field": "title",
        "headerContent": "Kid's name"
      }
    ],        
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
    "navLinks": True,
    "resourceGroupField": calendar_groupby,
    "resources": calendar_resources,
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
        strptime(time_str, '%H:%M')
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
    office_start_time = time(9, 0)
    office_end_time = time(18, 0)
    default_time_gap=15
    if default_time_gap < 15:
        default_time_gap=15

    date = st.date_input("Select the Date:", min_value=current_date,value=current_date)
    if date:
        start_times = [office_start_time]
        while start_times[-1] < office_end_time:
            next_time = (combine(date, start_times[-1]) + timedelta(minutes=default_time_gap)).time()
            start_times.append(next_time)  
      
        start_time = st.selectbox("Select the Start Time:", start_times,index=None)
        current_time = current_time_ist.time()
        if start_time:
            if (date == current_date and start_time < current_time):
                st.warning("Start time should be from current date and time.")
            else:
                end_of_day = min(office_end_time, time(23, 59))
                available_end_times = [datetime.combine(date, start_time) + timedelta(minutes=i) for i in range(default_time_gap, (end_of_day.hour - start_time.hour) * 60 + 1, default_time_gap)]
                formatted_end_times = [et.strftime('%H:%M') for et in available_end_times]
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

def form_time(item):
	try:
		return strptime(item, '%Y-%m-%d %H:%M:%S').time()
	except ValueError as ve1:
		try:
			return strptime(item, '%Y-%m-%dT%H:%M:%S').time()
		except ValueError as ve2:
			return ve2
		return ve1

# ======================================================================================================================================================================================================
@st.dialog("New Event")
def new_event(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Reason...")
    options = st.selectbox(f"Filter values for event:", data_cours_niveau['niveau_txt'],index=None)
    st.write("option=",options)
    try:
        st.write("value=",data_cours_niveau['niveau_txt'](options))
    except:
        st.write('None selected')
    #data_cours_filtered=dict(data_cours_niveau).loc[('niveau'>=option-1) & ('niveau'<=option+1)]
#df = df_chart.loc[(df_chart[xField] >= int(selMin)) & (df_chart[xField] <= int(selMax))]
    formatted_cours = [et['title'] + ': ' + form_time(et['start']).strftime('%H:%M') + '-' + form_time(et['end']).strftime('%H:%M') for et in list(data_cours)]
    requested_cours=st.selectbox("Select the period:", formatted_cours,index=None) 
  
    if st.button("Submit"):
        st.session_state.new_event = {"item": item, "reason": reason}
        st.rerun()

if "new_event" not in st.session_state:
    st.write("Create event")
    if st.button("New"):
        new_event("current_time_ist")
else:
    f"New event is {st.session_state.new_event['item']} for {st.session_state.new_event['reason']}"
# ======================================================================================================================================================================================================

st.title("Planning")

mode = st.selectbox("Calendar Mode:", options=list(calendar_display.keys()), format_func=lambda x:calendar_display[ x ])

if "resource" in mode:
    if mode == "resource-daygrid":
        calendar_options = {
            **calendar_options,
            "initialDate": initialDate,
            "initialView": "resourceDayGridDay",
            "firstweekday": 0,
            "resourceGroupField": calendar_groupby,
        }
    elif mode == "resource-timeline":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            },
            "initialDate": initialDate,
            "initialView": "resourceTimelineDay",
            "firstweekday": 0,
            "resourceGroupField": calendar_groupby,
        }
    elif mode == "resource-timegrid":
        calendar_options = {
            **calendar_options,
            "initialDate": initialDate,
            "initialView": "resourceTimeGridDay",
            "firstweekday": 0,
            "resourceGroupField": calendar_groupby,
        }
else:
    if mode == "daygrid":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "initialDate": initialDate,
            "initialView": "dayGridMonth",
            "firstweekday": 0,
        }
    elif mode == "timegrid":
        calendar_options = {
            **calendar_options,
            "initialView": "timeGridWeek",
        }
    elif mode == "timeline":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "timelineDay,timelineWeek,timelineMonth",
            },
            "initialDate": initialDate,
            "initialView": "timelineMonth",
        }
    elif mode == "list":
        calendar_options = {
            **calendar_options,
            "initialDate": initialDate,
            "initialView": "listMonth",
        }
    elif mode == "multimonth":
        calendar_options = {
            **calendar_options,
            "initialView": "multiMonthYear",
        }

planning = calendar(
        events=st.session_state.get("events", calendar_events),
        options=calendar_options,
        custom_css=calendar_custom_css,
        key=mode,
        )

if planning.get("eventsSet") is not None:
    st.session_state["events"] = planning["eventsSet"]

if st.button('Ungroup'):
    #planning.resourceGroupField=None
        pass
try:
        if "currentEnd" in planning['eventsSet']['view']:
                with st.expander('Calendar eventsSet', expanded=True, icon=':material/table_view:', width='stretch'):
                        #st.write(        planning['eventsSet']['view'].currentEnd[:10]        )
                        initialDate=planning['eventsSet']['view'].currentEnd
except:
        pass
        
with st.expander('Calendar data', expanded=False, icon=':material/table_view:', width='stretch'):
        st.write("Calendar data:", planning)

btn_txt_book='Book a meeting 🗓️'
menu_choice = st.selectbox("Menu", [btn_txt_book, "Cancel Booking", "View Bookings"])
if menu_choice == btn_txt_book:
    resa_book()

