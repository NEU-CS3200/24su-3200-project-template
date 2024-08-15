import logging
logger = logging.getLogger(__name__)
from datetime import date
import streamlit as st
from modules.nav import SideBarLinks
import requests
#from streamlit_calendar import calendar
st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome Student, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### Track Tasks and Scheduling Here')

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
