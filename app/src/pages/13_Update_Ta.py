import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title('Manage your availability')

st.write('**Check your current availability**')
with st.form("Current availability time slots"):
    ta_email = st.text_input('Email: ')

    submitted = st.form_submit_button('Check')
    if submitted:
        try:
        # ---- turn this into a header 
            st.write("Here is your current availability:")
            avail_data = requests.get(f'http://api:4000/a/avail/{ta_email}').json()
            st.dataframe(avail_data)
        except:
            st.write("Could not connect to the database to retrieve TA id! Make sure there are no typos in the form.")

st.write('')
st.write('**Add or delete your availability**')
# Create a form for adding or deleting a TA availability time slot
with st.form("Manage TA availability time slot"):
    ta_email = st.text_input('Email: ')
    avail_day = st.text_input('Day (Monday - Sunday): ')
    # ----- eventually, this could be a dropdown
    avail_time = st.text_input('Time (Morning, Afternoon, or Night): ')

    # Two submit buttons: one for adding and one for deleting
    add_submitted = st.form_submit_button('Add Availability')
    delete_submitted = st.form_submit_button('Delete Availability')

if add_submitted:
    data = {}
    data['time'] = avail_time     
    data['day'] = avail_day   
    st.write("Adding the following data:", data)

    # Send the POST request with the TA's email included in the URL
    response = requests.post(f'http://api:4000/a/{ta_email}', json=data)

    # Check the response from the server
    if response.status_code == 201:
        st.success('TA availability added successfully!')
    elif response.status_code == 404:
        st.error('TA or Availability not found!')
    else:
        st.error(f'Failed to add TA availability: {response.status_code}')

if delete_submitted:
    data = {}
    data['time'] = avail_time      
    data['day'] = avail_day   
    st.write("Deleting the following data:", data)

    # Send the POST request with the TA's email included in the URL
    response = requests.delete(f'http://api:4000/a/{ta_email}', json=data)

    # Check the response from the server
    if response.status_code == 200 or response.status_code == 204:
        st.success('TA availability deleted successfully!')
    elif response.status_code == 404:
        st.error('TA or Availability not found!')
    else:
        st.error(f'Failed to delete TA availability: {response.status_code}')
    # ----- need to add in DELETE call

# ------------- BREAK