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

# API Endpoints
API_BASE_URL = 'http://api:4000'

# Fetch sections assigned to the professor using the API
def fetch_sections(professor_id):
    response = requests.get(f'{API_BASE_URL}/p/professors/{professor_id}/sections')
    return response.json()

# Fetch sections assigned to the professor using the API
def fetch_students(section_num, semester_year):
    response = requests.get(f'{API_BASE_URL}/sec/sections/{section_num}/{semester_year}/students')
    return response.json()

if 'professor_id' not in st.session_state:
    st.error("Professor ID is not set. Please login or provide valid professor ID.")
else:
    professor_id = st.session_state['professor_id']

    # Display sections for the professor
    sections = fetch_sections(professor_id)
    st.write("### Sections")
    st.dataframe(pd.DataFrame(sections))

    if sections:
        section_options = []
        for section in sections:
            section_display = f"Section {section['section_num']} - {section['semester_year']}"
            section_options.append((section['section_num'], section['semester_year'], section_display))

        selected_section_display = st.selectbox(
        "Select a Section", 
        options=[option[2] for option in section_options]
    )
        # Find the corresponding section_num and semester_year based on the selected display string
        selected_section = next(option for option in section_options if option[2] == selected_section_display)

        if selected_section:
            section_num = selected_section[0]
            semester_year = selected_section[1]
            students = fetch_students(section_num, semester_year)
            st.write("### Students in this Section")
            st.dataframe(pd.DataFrame(students))  # Display students in a DataFrame
    else:
        st.write("No sections found.")


# Display blank DF initially for testing/ setup
st.write("### Blank DataFrame Example")
blank_df = pd.DataFrame()
st.dataframe(blank_df)

# Button to export data to a csv
if st.button('Export Data to CSV', type='primary', use_container_width=True):
    sections_df = pd.DataFrame(sections)
    sections_df.to_csv('exported_sections.csv', index=False)
    if students:
        students_df = pd.DataFrame(students)
        students_df.to_csv('exported_students.csv', index=False)
    st.success("Data exported to CSV files successfully!")

