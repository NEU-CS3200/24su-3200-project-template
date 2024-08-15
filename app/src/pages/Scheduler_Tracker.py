import logging
logger = logging.getLogger(__name__)
from datetime import date,datetime as dt
import streamlit as st
from modules.nav import SideBarLinks
import requests
from streamlit_calendar import calendar
st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome Student, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### Track Tasks and Scheduling Here')




#create calendar
calendar_options = {
    "editable": "true",
    "selectable": "true",
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "building",
    "resources": [
        {"id": "a", "building": "Building A", "title": "Building A"},
        {"id": "b", "building": "Building A", "title": "Building B"},
        {"id": "c", "building": "Building B", "title": "Building C"},
        {"id": "d", "building": "Building B", "title": "Building D"},
        {"id": "e", "building": "Building C", "title": "Building E"},
        {"id": "f", "building": "Building C", "title": "Building F"},
    ],
}


#starts = st.
calendar_events = [
    {
        "title": "Event 1",
        "start": "2024-08-31T08:30:00",
        "end": "2023-07-31T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "start": "2023-07-31T07:30:00",
        "end": "2023-07-31T10:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 3",
        "start": "2023-07-31T10:40:00",
        "end": "2023-07-31T12:30:00",
        "resourceId": "a",
    }
]

calendar = calendar(events=calendar_events, options=calendar_options)
st.write(calendar)

# Create a scheduling calendar
now = dt.now()
try:
    meetings = st.date_input(label='Schedule Meetings: ',
                value=(dt(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute),
                        dt(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute)),
                key='#date_range',
                help="The start and end date time")
    st.write('Start: ', dts[0], "End: ", dts[1])

except:
    pass


# Function to add a new task with a date
def load_tasks():
    if "tasks" not in st.session_state:
        st.session_state.tasks = []


def add_task():
    if st.session_state.new_task and st.session_state.task_date:
        task = {
            "task": st.session_state.new_task,
            "date": st.session_state.task_date
        }
        st.session_state.tasks.append(task)
        st.session_state.new_task = ""
        st.session_state.task_date = date.today()

# Function to remove a task
def remove_task(task):
    st.session_state.tasks.remove(task)

# Load existing tasks
load_tasks()

# Title of the app
st.title("To-Do List")

# Input for a new task
st.text_input("New Task", key="new_task")

# Date input for the task
st.date_input("Due Date", key="task_date", value=date.today())

# Button to add the task
st.button("Add Task", on_click=add_task)

# Display the tasks
if st.session_state.tasks:
    st.write("### Your Tasks")
    for task in st.session_state.tasks:
        task_description = f"- {task['task']} (Due: {task['date']})"
        st.write(task_description, key=task['task'])
        st.button(f"Remove {task['task']}", key=f"remove_{task['task']}", on_click=remove_task, args=(task,))
