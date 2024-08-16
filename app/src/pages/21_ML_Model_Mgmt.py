
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()


st.title('Update student groups')
st.write('')
st.write('**See the current groups**')
st.write('Enter your information in the form below:')

with st.form("See students groups"):
  prof_email = st.text_input('Email: ')

  submitted = st.form_submit_button('Submit')

if submitted:
    st.write(f"Email: {prof_email}")
    # --- need to get this to return the specfic TA's availability 
    try:
        # ---- turn this into a header 
        st.write("Here are the students groups in your sections:")
        group_data = requests.get(f'http://api:4000/p/{prof_email}/groups').json()
        st.dataframe(group_data)
    except:
        st.write("Could not connect to the database to retrieve professor id! Make sure there are no typos in the form.")

st.write('')
st.write('**Update student group assignment**')
st.write('Enter your information in the form below:')
with st.form("Manage student groups"):
    #prof_email = st.text_input('Email: ')
    student_email = st.text_input('Student Email (email of the student you wish to update!): ')
    new_group = st.text_input('Name of New Group: ')
    # Two submit buttons: one for adding and one for deleting
    updated = st.form_submit_button('Update')

if updated:
    data = {}
    data['email'] = student_email  
    data['group_name'] = new_group
    st.write("Entered data:", data)

    # Send the put request! 
    response = requests.put(f'http://api:4000/p/student/{new_group}/{student_email}', json=data)

    # Check the response from the server
    if response.status_code == 201:
        st.success('Group updated!')
    elif response.status_code == 404:
        st.error('Student not found!')
    else:
        st.error(f'Failed to update group: {response.status_code}')


# # Step 1: Enter Professor ID
# professor_id = st.text_input('Enter Professor ID:')

# if professor_id:
#     # Step 2: Select Section
#     section_response = requests.get(f'http://api:4000/sec/{professor_id}/sections')
#     if section_response.status_code == 200:
#         sections = section_response.json()
#         section_options = [(section['section_num'], section['course_name']) for section in sections]
        
#         selected_section = st.selectbox('Select Section', section_options)
        
#         if selected_section:
#             section_num, course_name = selected_section
            
#             # Step 3: Fetch Students in Section
#             students_api_url = f'http://api:4000/sec/sections/{section_num}/students'
            
#             student_response = requests.get(students_api_url)
            
#             if student_response.status_code == 200:
#                 students = student_response.json()
#                 student_options = [(student['student_id'], f"{student['first_name']} {student['last_name']}") for student in students]
                
#                 selected_student = st.selectbox('Select Student', student_options)
                
#                 if selected_student:
#                     # Step 4: Perform any other action on selected student
#                     st.write(f"Selected Student: {selected_student}")
#             else:
#                 st.error(f'Failed to load students. Status Code: {student_response.status_code}')
#     else:
#         st.error('Failed to load sections.')
