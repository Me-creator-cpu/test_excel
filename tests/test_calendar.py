import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import csv
import pandas as pd
from pytz import timezone


st.title("Editable & Selectable Calendar")

options = {
    "editable": True,
    "selectable": True,
    "initialView": "dayGridMonth",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,listMonth"
    }
}

events = [
    {"title": "Conference", "start": "2025-09-15", "end": "2025-09-17"},
    {"title": "Team Meeting", "start": "2025-09-21", "end": "2025-09-21"}
]

cal_data = calendar(events=events, options=options, key="basic_cal")
st.write("Interaction data:", cal_data)