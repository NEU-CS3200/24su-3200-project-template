import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
from datetime import datetime as dt,time
#from streamlit_calendar import calendar

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.title('Update your major')

st.write('Enter your information in the form below:')
with st.form("Update Major"):
    fname = st.text_input('First Name: ')
    lname = st.text_input('Last Name: ')
    email = st.text_input('Email: ')
    major = st.text_input('Updated Major: ')

    # Two submit buttons: one for adding and one for deleting
    submitted = st.form_submit_button('Update')

if submitted:
    data = {}
    data['first_name'] = fname    
    data['last_name'] = lname 
    data['email'] = email 
    st.write("Updating the major for you:", data)

    # Send the put request! 
    response = requests.put(f'http://api:4000/s/students/{fname}/{lname}/{email}/{major}', json=data)

    # Check the response from the server
    if response.status_code == 200:
        st.success('Major updated!')
    elif response.status_code == 404:
        st.error('Student not found!')
    else:
        st.error(f'Failed to update major: {response.status_code}')


# # create a text entry field
# with st.form("Update your information"):
#     f_name = st.text_input("First Name:")
#     l_name = st.text_input("Last Name:")
#     email = st.text_input("Enter your Email:")
#     major = st.text_input("Enter your Major:")
#     year = st.selectbox("What year are you",options=(1,2,3,4,5))
#     dorm = st.selectbox("Do you live on or Off Campus?",options=('True','False'))

#     # # insert into availiblity table
#     # time = st.selectbox(label = 'What Time Of Day?',options=('Morning','Afternoon','Night'))
#     # days = st.multiselect("What Days Can you Meet?",
#     #                       options=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'))

#     updated = st.form_submit_button("Update")
# # Upon submission Update the Database with the information by using a put request
#     if updated:
#         data = {}
#         data['f_name'] = f_name
#         data['l_name'] = l_name
#         data['email'] = email
#         data['day'] = major
#         data['year'] = year
#         data['dorm'] = dorm
#         # ----- need to add in 
#         response = requests.post('',json=data)

#         if response.status_code == 200:
#             st.write("Form Submitted Sucessfully")
#         else:
#             st.write("Failed to Submit")

#         if submitted:
#             aval_data ={}
#             aval_data['time'] = time
#             aval_data['days'] = days

#             response = requests.post('http://api:4000/sa/stuAvailability',json=data)

#     if updated:
#         data_u = {}
#         data['f_name'] = f_name
#         data['l_name'] = l_name
#         data['email'] = email
#         data['major'] = major
#         data['interests'] = interests
#         data['year'] = year
#         data['dorm'] = dorm

#         response = requests.put('http://api:4000/s/students',json=data_u)

#         if response.status_code == 200:
#             st.write("Form Updated Sucessfully")
#         else:
#             st.write("Failed Update Submit")

#         if updated:
#             aval_data_u ={}
#             aval_data['time'] = time
#             aval_data['days'] = days

#             response = requests.put('http://api:4000/sa/stuAvailability',json=aval_data_u)





# st.title('Manage your availability')

# st.write('**Check your current availability**')
# with st.form("Current availability time slots"):
#     email = st.text_input('Email: ')

#     submitted = st.form_submit_button('Check')
#     if submitted:
#         try:
#         # ---- turn this into a header 
#             st.write("Here is your current availability:")
#             avail_data = requests.get(f'http://api:4000/a/avail/{email}').json()
#             st.dataframe(avail_data)
#         except:
#             st.write("Could not connect to the database to retrieve TA id! Make sure there are no typos in the form.")

# st.write('')
# st.write('**Add availability**')
# # Create a form for adding or deleting a TA availability time slot
# with st.form("Manage your availability time slot"):
#     ta_email = st.text_input('Email: ')
#     avail_day = st.text_input('Day (Monday - Sunday): ')
#     # ----- eventually, this could be a dropdown
#     avail_time = st.text_input('Time (Morning, Afternoon, or Night): ')

#     # Two submit buttons: one for adding and one for deleting
#     add_submitted = st.form_submit_button('Add')

# if add_submitted:
#     data = {}
#     data['time'] = avail_time     
#     data['day'] = avail_day   
#     st.write("Adding the following data:", data)

#     # Send the POST request with the TA's email included in the URL
#     response = requests.post(f'http://api:4000/a/{ta_email}', json=data)

#     # Check the response from the server
#     if response.status_code == 201:
#         st.success('TA availability added successfully!')
#     elif response.status_code == 404:
#         st.error('TA or Availability not found!')
#     else:
#         st.error(f'Failed to add TA availability: {response.status_code}')
