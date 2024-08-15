import logging
logger = logging.getLogger(__name__)
from datetime import date,datetime as dt,timedelta
import streamlit as st
from modules.nav import SideBarLinks
import requests
from streamlit_calendar import calendar
st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Student, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### Track Tasks and Scheduling Here')


# Initialize a dictionary to hold the events
if "events" not in st.session_state:
    st.session_state.events = []

# Title of the app
st.title("Editable Calendar")

# Display the calendar
selected_date = calendar(events=st.session_state.events)
start_date = st.text_input("Input in the following format '2024-09-01'")

# Add Event
event_title = st.text_input("Event Title")
if st.button("Add Event"):
    new_event = {
        "title": event_title,
        "start": start_date
    }
    st.session_state.events.append(new_event)

# Delete Events
if st.button("Delete Event"):
    remove_event = {
        "title": event_title,
        "start": start_date
    }
    st.session_state.events.remove(remove_event)





