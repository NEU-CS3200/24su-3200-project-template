import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Accessing a REST API from Within Streamlit")

"""
Simply retrieving data from a REST api running in a separate Docker Container.

If the container isn't running, this will be very unhappy.  But the Streamlit app 
should not totally die. 
"""
data = {} 
url = 'http://localhost:4000/u/users'
    
try:
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print("Successfully connected to the API.")
        print("Data retrieved:", data)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print("Response:", response.text)
except requests.exceptions.RequestException as e:
    # Handle any exceptions that might occur
    print("An error occurred while trying to connect to the API:")
    print(str(e))
    st.write("**Important**: Could not connect to sample api, so using dummy data.")
    data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}


st.dataframe(data)


