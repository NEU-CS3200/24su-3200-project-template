import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Professor Home Page')
st.write(f"Welcome, {st.session_state.get('first_name', 'Professor')}!")

# connect to project pal database

# Fetch sections assigned to the professor using the API
def fetch_sections(professor_id):
    response = requests.get(f'http://api:4000/p/professors/{professor_id}/sections')
    return response.json()

# Fetch sections assigned to the professor using the API
def fetch_students(section_id):
    response = requests.get(f'http://api:4000/sec/sections/{section_id}/students')
    return response.json()

# Display sections for the professor
sections = fetch_sections(st.session_state['professor_id'])
st.write("### Sections")
st.dataframe(sections)

# Allow Professor to select a section and view students
section_id = st.selectbox("Select a Section", [section['section_id'] for section in sections])
if section_id:
    students = fetch_students(section_id)
    st.write("### Students in this Section")
    st.dataframe(students)

# Button to export data to a csv
if st.button('Export Data to CSV', type='primary', use_container_width=True):
    sections_df = pd.DataFrame(sections)
    sections_df.to_csv('exported_sections.csv', index=False)
    if students:
        students_df = pd.DataFrame(students)
        students_df.to_csv('exported_students.csv', index=False)
    st.success("Data exported to CSV files successfully!")

