
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()


st.title('Update Students and Groups')

# Step 1: Enter Professor ID
professor_id = st.text_input('Enter Professor ID:')

if professor_id:
    # Step 2: Select Section
    section_response = requests.get(f'http://api:4000/sec/{professor_id}/sections')
    if section_response.status_code == 200:
        sections = section_response.json()
        section_options = [(section['section_num'], section['course_name']) for section in sections]
        
        selected_section = st.selectbox('Select Section', section_options)
        
        if selected_section:
            section_num, course_name = selected_section
            
            # Step 3: Fetch Students in Section
            students_api_url = f'http://api:4000/sec/sections/{section_num}/students'
            
            student_response = requests.get(students_api_url)
            
            if student_response.status_code == 200:
                students = student_response.json()
                student_options = [(student['student_id'], f"{student['first_name']} {student['last_name']}") for student in students]
                
                selected_student = st.selectbox('Select Student', student_options)
                
                if selected_student:
                    # Step 4: Perform any other action on selected student
                    st.write(f"Selected Student: {selected_student}")
            else:
                st.error(f'Failed to load students. Status Code: {student_response.status_code}')
    else:
        st.error('Failed to load sections.')
