import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

SideBarLinks()

# ----------- this just gets the sections that a given professor is teaching 
st.title('See My Students')
st.write('')
st.write('Feel free to sort by section in the data below')
with st.form("Section Data "):
  prof_id = st.text_input('ID: ')

  submitted = st.form_submit_button('Submit')

st.write('')
if submitted:
    st.write(f"Your ID: {prof_id}")
    try:
        # ---- turn this into a header 
        st.write("Here are the current sections:")
        students_data = requests.get(f'http://api:4000/sec/{prof_id}/students').json()
        st.dataframe(students_data)
    except:
        st.write("Could not connect to the database to get your students, you may not be teaching a section.")

# # Fetch sections assigned to the professor using the API
# def fetch_sections(professor_id):
#     response = requests.get(f'http://api:4000/p/professors/{professor_id}/sections')
#     return response.json()

# # Fetch sections assigned to the professor using the API
# def fetch_students(section_id):
#     response = requests.get(f'http://api:4000/sec/sections/{section_id}/students')
#     return response.json()

# # Display sections for the professor
# sections = fetch_sections(st.session_state['professor_id'])
# st.write("### Sections")
# st.dataframe(sections)

# # Allow Professor to select a section and view students
# section_id = st.selectbox("Select a Section", [section['section_id'] for section in sections])
# if section_id:
#     students = fetch_students(section_id)
#     st.write("### Students in this Section")
#     st.dataframe(students)

# # Button to export data to a csv
# if st.button('Export Data to CSV', type='primary', use_container_width=True):
#     sections_df = pd.DataFrame(sections)
#     sections_df.to_csv('exported_sections.csv', index=False)
#     if students:
#         students_df = pd.DataFrame(students)
#         students_df.to_csv('exported_students.csv', index=False)
#     st.success("Data exported to CSV files successfully!")